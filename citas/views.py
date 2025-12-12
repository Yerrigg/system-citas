from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Cita
from doctores.models import Doctor
from especialidades.models import Especialidad
from pacientes.models import Paciente
from horarios.models import Horario
from django.core.exceptions import ValidationError

@login_required
def lista_especialidades(request):
    """Muestra todas las especialidades disponibles"""
    especialidades = Especialidad.objects.filter(activo=True)
    return render(request, 'citas/lista_especialidades.html', {
        'especialidades': especialidades
    })

@login_required
def lista_doctores(request, especialidad_id=None):
    """Muestra doctores filtrados por especialidad"""
    doctores = Doctor.objects.filter(activo=True)
    especialidad = None
    
    if especialidad_id:
        especialidad = get_object_or_404(Especialidad, id=especialidad_id)
        doctores = doctores.filter(especialidades=especialidad)
    
    return render(request, 'citas/lista_doctores.html', {
        'doctores': doctores,
        'especialidad': especialidad
    })

@login_required
def disponibilidad_doctor(request, doctor_id):
    """Muestra la disponibilidad del doctor y permite agendar"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Obtener horarios del doctor
    horarios = Horario.objects.filter(doctor=doctor, activo=True)
    
    # Obtener citas ya agendadas (próximos 30 días)
    fecha_inicio = timezone.now().date()
    fecha_fin = fecha_inicio + timedelta(days=30)
    citas_agendadas = Cita.objects.filter(
        doctor=doctor,
        fecha__range=[fecha_inicio, fecha_fin]
    ).exclude(estado='cancelada')
    
    return render(request, 'citas/disponibilidad_doctor.html', {
        'doctor': doctor,
        'horarios': horarios,
        'citas_agendadas': citas_agendadas,
        'today': timezone.now().date(), 
    })

@login_required
def agendar_cita(request, doctor_id):
    """Procesa el formulario para agendar una cita"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Verificar que el usuario tenga un perfil de paciente
    try:
        paciente = request.user.paciente
    except:
        messages.error(request, 'Debes tener un perfil de paciente para agendar citas.')
        return redirect('home')
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        motivo = request.POST.get('motivo')
        tipo = request.POST.get('tipo', 'primera_vez')
        
        try:
            # Convertir a objetos de fecha y hora
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
            
            # Calcular hora_fin (sumar duración de la especialidad)
            duracion = doctor.especialidades.first().duracion_cita if doctor.especialidades.exists() else 30
            hora_fin_obj = (datetime.combine(fecha_obj, hora_inicio_obj) + timedelta(minutes=duracion)).time()
            
            # Crear la cita (se ejecutarán las validaciones automáticamente)
            cita = Cita(
                paciente=paciente,
                doctor=doctor,
                fecha=fecha_obj,
                hora_inicio=hora_inicio_obj,
                hora_fin=hora_fin_obj,
                tipo=tipo,
                motivo=motivo,
                estado='pendiente'
            )
            
            # Validar antes de guardar
            cita.clean()
            cita.save()
            
            messages.success(request, f'¡Cita agendada exitosamente para el {fecha} a las {hora_inicio}!')
            return redirect('mis_citas')
            
        except ValidationError as e:
            # Mostrar errores de validación
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('disponibilidad_doctor', doctor_id=doctor.id)
        
        except Exception as e:
            messages.error(request, f'Error al agendar la cita: {str(e)}')
            return redirect('disponibilidad_doctor', doctor_id=doctor.id)
    
    return redirect('disponibilidad_doctor', doctor_id=doctor.id)

@login_required
def mis_citas(request):
    """Muestra las citas del paciente"""
    try:
        paciente = request.user.paciente
        citas = Cita.objects.filter(paciente=paciente).order_by('-fecha', '-hora_inicio')
        
        return render(request, 'citas/mis_citas.html', {
            'citas': citas
        })
    except:
        messages.error(request, 'No tienes un perfil de paciente.')
        return redirect('home')

@login_required
def detalle_cita(request, cita_id):
    """Muestra el detalle de una cita"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificar que el usuario sea el dueño de la cita
    if hasattr(request.user, 'paciente') and cita.paciente == request.user.paciente:
        return render(request, 'citas/detalle_cita.html', {'cita': cita})
    elif hasattr(request.user, 'doctor') and cita.doctor == request.user.doctor:
        return render(request, 'citas/detalle_cita.html', {'cita': cita})
    else:
        messages.error(request, 'No tienes permiso para ver esta cita.')
        return redirect('home')

@login_required
def cancelar_cita(request, cita_id):
    """Cancela una cita"""
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificar que el usuario sea el dueño de la cita
    if hasattr(request.user, 'paciente') and cita.paciente == request.user.paciente:
        if cita.estado in ['pendiente', 'confirmada']:
            cita.estado = 'cancelada'
            cita.save()
            messages.success(request, 'Cita cancelada exitosamente.')
        else:
            messages.error(request, 'No se puede cancelar esta cita.')
        return redirect('mis_citas')
    else:
        messages.error(request, 'No tienes permiso para cancelar esta cita.')
        return redirect('home')