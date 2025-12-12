from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count
from .models import Doctor
from citas.models import Cita
from horarios.models import Horario, Excepcion
from pacientes.models import Paciente
from django.db.models import Q

@login_required
def dashboard_doctor(request):
    """Dashboard principal del doctor"""
    # Verificar que el usuario sea doctor
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    # Fecha actual
    hoy = timezone.now().date()
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(
        doctor=doctor,
        fecha=hoy
    ).exclude(estado='cancelada').order_by('hora_inicio')
    
    # Próximas citas (próximos 7 días)
    proximas_citas = Cita.objects.filter(
        doctor=doctor,
        fecha__range=[hoy, hoy + timedelta(days=7)]
    ).exclude(estado='cancelada').order_by('fecha', 'hora_inicio')[:10]
    
    # Estadísticas
    total_citas_mes = Cita.objects.filter(
        doctor=doctor,
        fecha__month=hoy.month,
        fecha__year=hoy.year
    ).exclude(estado='cancelada').count()
    
    citas_completadas = Cita.objects.filter(
        doctor=doctor,
        estado='completada',
        fecha__month=hoy.month
    ).count()
    
    citas_pendientes = Cita.objects.filter(
        doctor=doctor,
        estado__in=['pendiente', 'confirmada'],
        fecha__gte=hoy
    ).count()
    
    # Pacientes atendidos este mes
    pacientes_mes = Cita.objects.filter(
        doctor=doctor,
        fecha__month=hoy.month,
        fecha__year=hoy.year,
        estado='completada'
    ).values('paciente').distinct().count()
    
    context = {
        'doctor': doctor,
        'citas_hoy': citas_hoy,
        'proximas_citas': proximas_citas,
        'total_citas_mes': total_citas_mes,
        'citas_completadas': citas_completadas,
        'citas_pendientes': citas_pendientes,
        'pacientes_mes': pacientes_mes,
    }
    
    return render(request, 'doctores/dashboard.html', context)

@login_required
def agenda_doctor(request):
    """Agenda completa del doctor con filtros"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    estado = request.GET.get('estado')
    
    # Query base
    citas = Cita.objects.filter(doctor=doctor)
    
    # Aplicar filtros
    if fecha_inicio:
        citas = citas.filter(fecha__gte=fecha_inicio)
    else:
        # Por defecto, mostrar desde hoy
        citas = citas.filter(fecha__gte=timezone.now().date())
    
    if fecha_fin:
        citas = citas.filter(fecha__lte=fecha_fin)
    else:
        # Por defecto, mostrar próximos 30 días
        citas = citas.filter(fecha__lte=timezone.now().date() + timedelta(days=30))
    
    if estado:
        citas = citas.filter(estado=estado)
    
    citas = citas.order_by('fecha', 'hora_inicio')
    
    # Horarios del doctor
    horarios = Horario.objects.filter(doctor=doctor, activo=True)
    
    context = {
        'doctor': doctor,
        'citas': citas,
        'horarios': horarios,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'estado': estado,
    }
    
    return render(request, 'doctores/agenda.html', context)

@login_required
def atender_cita(request, cita_id):
    """Atender una cita - Agregar diagnóstico y tratamiento"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificar que sea el doctor de la cita
    try:
        if cita.doctor != request.user.doctor:
            messages.error(request, 'No tienes permiso para atender esta cita.')
            return redirect('dashboard_doctor')
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    if request.method == 'POST':
        notas = request.POST.get('notas')
        diagnostico = request.POST.get('diagnostico')
        tratamiento = request.POST.get('tratamiento')
        
        # Actualizar cita
        cita.notas = notas
        cita.diagnostico = diagnostico
        cita.tratamiento = tratamiento
        cita.estado = 'completada'
        cita.save()
        
        messages.success(request, 'Cita atendida exitosamente.')
        return redirect('dashboard_doctor')
    
    return render(request, 'doctores/atender_cita.html', {'cita': cita})

@login_required
def mis_pacientes(request):
    """Lista de pacientes atendidos por el doctor"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    # Obtener pacientes únicos que han tenido citas con este doctor
    pacientes_ids = Cita.objects.filter(
        doctor=doctor
    ).values_list('paciente_id', flat=True).distinct()
    
    pacientes = Paciente.objects.filter(id__in=pacientes_ids)
    
    # Agregar información adicional
    pacientes_data = []
    for paciente in pacientes:
        total_citas = Cita.objects.filter(
            doctor=doctor,
            paciente=paciente
        ).count()
        
        ultima_cita = Cita.objects.filter(
            doctor=doctor,
            paciente=paciente
        ).order_by('-fecha', '-hora_inicio').first()
        
        pacientes_data.append({
            'paciente': paciente,
            'total_citas': total_citas,
            'ultima_cita': ultima_cita,
        })
    
    context = {
        'doctor': doctor,
        'pacientes_data': pacientes_data,
    }
    
    return render(request, 'doctores/mis_pacientes.html', context)

@login_required
def historial_paciente(request, paciente_id):
    """Ver historial completo de un paciente"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Obtener todas las citas del paciente con este doctor
    citas = Cita.objects.filter(
        doctor=doctor,
        paciente=paciente
    ).order_by('-fecha', '-hora_inicio')
    
    context = {
        'doctor': doctor,
        'paciente': paciente,
        'citas': citas,
    }
    
    return render(request, 'doctores/historial_paciente.html', context)

@login_required
def gestionar_horarios(request):
    """Gestionar horarios del doctor"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    if request.method == 'POST':
        # Procesar nuevo horario
        dia_semana = request.POST.get('dia_semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        # Validar que no exista conflicto
        conflicto = Horario.objects.filter(
            doctor=doctor,
            dia_semana=dia_semana,
            activo=True
        ).filter(
            Q(hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio)
        ).exists()
        
        if conflicto:
            messages.error(request, 'Ya existe un horario que se solapa con este.')
        else:
            Horario.objects.create(
                doctor=doctor,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                activo=True
            )
            messages.success(request, 'Horario agregado exitosamente.')
        
        return redirect('gestionar_horarios')
    
    horarios = Horario.objects.filter(doctor=doctor).order_by('dia_semana', 'hora_inicio')
    excepciones = Excepcion.objects.filter(doctor=doctor).order_by('-fecha_inicio')
    
    context = {
        'doctor': doctor,
        'horarios': horarios,
        'excepciones': excepciones,
    }
    
    return render(request, 'doctores/gestionar_horarios.html', context)

@login_required
def eliminar_horario(request, horario_id):
    """Eliminar un horario"""
    horario = get_object_or_404(Horario, id=horario_id)
    
    try:
        if horario.doctor == request.user.doctor:
            horario.delete()
            messages.success(request, 'Horario eliminado exitosamente.')
        else:
            messages.error(request, 'No tienes permiso para eliminar este horario.')
    except:
        messages.error(request, 'Error al eliminar el horario.')
    
    return redirect('gestionar_horarios')

@login_required
def agregar_excepcion(request):
    """Agregar excepción (vacaciones, bloqueos)"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'No tienes un perfil de doctor.')
        return redirect('home')
    
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        motivo = request.POST.get('motivo')
        descripcion = request.POST.get('descripcion')
        
        Excepcion.objects.create(
            doctor=doctor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            motivo=motivo,
            descripcion=descripcion
        )
        
        messages.success(request, 'Excepción agregada exitosamente.')
        return redirect('gestionar_horarios')
    
    return redirect('gestionar_horarios')

@login_required
def confirmar_cita(request, cita_id):
    """Confirmar una cita pendiente"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    try:
        if cita.doctor == request.user.doctor:
            if cita.estado == 'pendiente':
                cita.estado = 'confirmada'
                cita.save()
                messages.success(request, 'Cita confirmada exitosamente.')
            else:
                messages.info(request, 'La cita ya ha sido confirmada.')
        else:
            messages.error(request, 'No tienes permiso para confirmar esta cita.')
    except:
        messages.error(request, 'Error al confirmar la cita.')
    
    return redirect('dashboard_doctor')

@login_required
def marcar_no_asistio(request, cita_id):
    """Marcar que el paciente no asistió"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    try:
        if cita.doctor == request.user.doctor:
            cita.estado = 'no_asistio'
            cita.save()
            messages.success(request, 'Cita marcada como "No asistió".')
        else:
            messages.error(request, 'No tienes permiso para modificar esta cita.')
    except:
        messages.error(request, 'Error al modificar la cita.')
    
    return redirect('dashboard_doctor')


@login_required
def buscar_doctores(request):
    """Búsqueda avanzada de doctores"""
    
    # Obtener parámetros de búsqueda
    query = request.GET.get('q', '')
    especialidad_id = request.GET.get('especialidad')
    
    # Query base
    doctores = Doctor.objects.filter(activo=True)
    
    # Búsqueda por nombre
    if query:
        doctores = doctores.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(licencia_medica__icontains=query)
        )
    
    # Filtrar por especialidad
    if especialidad_id:
        doctores = doctores.filter(especialidades__id=especialidad_id)
    
    # Evitar duplicados
    doctores = doctores.distinct()
    
    # Especialidades para el filtro
    from especialidades.models import Especialidad
    especialidades = Especialidad.objects.filter(activo=True)
    
    context = {
        'doctores': doctores,
        'especialidades': especialidades,
        'query': query,
        'especialidad_id': especialidad_id,
    }
    
    return render(request, 'doctores/buscar_doctores.html', context)