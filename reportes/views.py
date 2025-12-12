from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncDate
from datetime import datetime, timedelta
from django.http import HttpResponse
import json

from citas.models import Cita
from doctores.models import Doctor
from pacientes.models import Paciente
from especialidades.models import Especialidad
from usuarios.models import Usuario

# Verificar que sea administrador
def es_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(es_admin)
def dashboard_admin(request):
    """Dashboard principal de administración con estadísticas"""
    
    # Fechas para filtros
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Filtros de fecha
    fecha_inicio_param = request.GET.get('fecha_inicio')
    fecha_fin_param = request.GET.get('fecha_fin')
    
    if fecha_inicio_param:
        fecha_inicio = datetime.strptime(fecha_inicio_param, '%Y-%m-%d').date()
    else:
        fecha_inicio = inicio_mes
        
    if fecha_fin_param:
        fecha_fin = datetime.strptime(fecha_fin_param, '%Y-%m-%d').date()
    else:
        fecha_fin = hoy
    
    # Estadísticas generales
    total_pacientes = Paciente.objects.filter(activo=True).count()
    total_doctores = Doctor.objects.filter(activo=True).count()
    total_especialidades = Especialidad.objects.filter(activo=True).count()
    
    # Citas en el rango de fechas
    citas_periodo = Cita.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin]
    )
    
    total_citas = citas_periodo.count()
    citas_completadas = citas_periodo.filter(estado='completada').count()
    citas_pendientes = citas_periodo.filter(estado__in=['pendiente', 'confirmada']).count()
    citas_canceladas = citas_periodo.filter(estado='cancelada').count()
    citas_no_asistio = citas_periodo.filter(estado='no_asistio').count()
    
    # Porcentajes
    if total_citas > 0:
        tasa_completadas = round((citas_completadas / total_citas) * 100, 1)
        tasa_canceladas = round((citas_canceladas / total_citas) * 100, 1)
        tasa_no_asistio = round((citas_no_asistio / total_citas) * 100, 1)
    else:
        tasa_completadas = 0
        tasa_canceladas = 0
        tasa_no_asistio = 0
    
    # Citas por especialidad (Top 5)
    citas_por_especialidad = []
    especialidades = Especialidad.objects.filter(activo=True)
    for esp in especialidades:
        total = citas_periodo.filter(doctor__especialidades=esp).count()
        if total > 0:
            citas_por_especialidad.append({
                'nombre': esp.nombre,
                'total': total
            })
    citas_por_especialidad.sort(key=lambda x: x['total'], reverse=True)
    citas_por_especialidad = citas_por_especialidad[:5]
    
    # Doctores más solicitados (Top 5)
    doctores_mas_solicitados = []
    doctores = Doctor.objects.filter(activo=True)[:10]
    for doc in doctores:
        total = citas_periodo.filter(doctor=doc).count()
        if total > 0:
            doctores_mas_solicitados.append({
                'nombre': doc.usuario.get_full_name(),
                'total': total
            })
    doctores_mas_solicitados.sort(key=lambda x: x['total'], reverse=True)
    doctores_mas_solicitados = doctores_mas_solicitados[:5]
    
    # Citas por mes (últimos 6 meses)
    hace_6_meses = hoy - timedelta(days=180)
    citas_por_mes = Cita.objects.filter(
        fecha__gte=hace_6_meses
    ).annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Nuevos pacientes por mes
    pacientes_por_mes = Paciente.objects.filter(
        created_at__gte=hace_6_meses
    ).annotate(
        mes=TruncMonth('created_at')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    # Horarios pico (horas más ocupadas)
    horarios_pico = citas_periodo.values(
        'hora_inicio'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    context = {
        'total_pacientes': total_pacientes,
        'total_doctores': total_doctores,
        'total_especialidades': total_especialidades,
        'total_citas': total_citas,
        'citas_completadas': citas_completadas,
        'citas_pendientes': citas_pendientes,
        'citas_canceladas': citas_canceladas,
        'citas_no_asistio': citas_no_asistio,
        'tasa_completadas': tasa_completadas,
        'tasa_canceladas': tasa_canceladas,
        'tasa_no_asistio': tasa_no_asistio,
        'citas_por_especialidad': citas_por_especialidad,
        'doctores_mas_solicitados': doctores_mas_solicitados,
        'citas_por_mes': citas_por_mes,
        'pacientes_por_mes': pacientes_por_mes,
        'horarios_pico': horarios_pico,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'reportes/dashboard_admin.html', context)

@login_required
@user_passes_test(es_admin)
def reporte_citas(request):
    """Reporte detallado de citas"""
    
    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    especialidad_id = request.GET.get('especialidad')
    doctor_id = request.GET.get('doctor')
    estado = request.GET.get('estado')
    
    # Query base
    citas = Cita.objects.all()
    
    # Aplicar filtros
    if fecha_inicio:
        citas = citas.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        citas = citas.filter(fecha__lte=fecha_fin)
    if especialidad_id:
        citas = citas.filter(doctor__especialidades__id=especialidad_id)
    if doctor_id:
        citas = citas.filter(doctor_id=doctor_id)
    if estado:
        citas = citas.filter(estado=estado)
    
    citas = citas.select_related(
        'paciente__usuario',
        'doctor__usuario'
    ).order_by('-fecha', '-hora_inicio')
    
    # Para los filtros
    especialidades = Especialidad.objects.filter(activo=True)
    doctores = Doctor.objects.filter(activo=True).select_related('usuario')
    
    context = {
        'citas': citas,
        'especialidades': especialidades,
        'doctores': doctores,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'especialidad_id': especialidad_id,
        'doctor_id': doctor_id,
        'estado': estado,
    }
    
    return render(request, 'reportes/reporte_citas.html', context)

@login_required
@user_passes_test(es_admin)
def reporte_doctores(request):
    """Reporte de rendimiento de doctores"""
    
    fecha_inicio_param = request.GET.get('fecha_inicio')
    fecha_fin_param = request.GET.get('fecha_fin')
    
    # Si no hay fechas, usar el mes actual
    hoy = timezone.now().date()
    if fecha_inicio_param:
        fecha_inicio = datetime.strptime(fecha_inicio_param, '%Y-%m-%d').date()
    else:
        fecha_inicio = hoy.replace(day=1)
        
    if fecha_fin_param:
        fecha_fin = datetime.strptime(fecha_fin_param, '%Y-%m-%d').date()
    else:
        fecha_fin = hoy
    
    # Obtener doctores con estadísticas
    doctores = Doctor.objects.filter(activo=True)
    
    doctores_data = []
    for doctor in doctores:
        citas_totales = Cita.objects.filter(
            doctor=doctor,
            fecha__range=[fecha_inicio, fecha_fin]
        ).count()
        
        citas_completadas = Cita.objects.filter(
            doctor=doctor,
            fecha__range=[fecha_inicio, fecha_fin],
            estado='completada'
        ).count()
        
        citas_canceladas = Cita.objects.filter(
            doctor=doctor,
            fecha__range=[fecha_inicio, fecha_fin],
            estado='cancelada'
        ).count()
        
        citas_no_asistio = Cita.objects.filter(
            doctor=doctor,
            fecha__range=[fecha_inicio, fecha_fin],
            estado='no_asistio'
        ).count()
        
        pacientes_atendidos = Cita.objects.filter(
            doctor=doctor,
            fecha__range=[fecha_inicio, fecha_fin],
            estado='completada'
        ).values('paciente').distinct().count()
        
        # Porcentajes
        if citas_totales > 0:
            tasa_completadas = round((citas_completadas / citas_totales) * 100, 1)
            tasa_efectividad = round(((citas_totales - citas_canceladas - citas_no_asistio) / citas_totales) * 100, 1)
        else:
            tasa_completadas = 0
            tasa_efectividad = 0
        
        doctores_data.append({
            'doctor': doctor,
            'citas_totales': citas_totales,
            'citas_completadas': citas_completadas,
            'citas_canceladas': citas_canceladas,
            'citas_no_asistio': citas_no_asistio,
            'pacientes_atendidos': pacientes_atendidos,
            'tasa_completadas': tasa_completadas,
            'tasa_efectividad': tasa_efectividad,
        })
    
    # Ordenar por citas totales
    doctores_data.sort(key=lambda x: x['citas_totales'], reverse=True)
    
    context = {
        'doctores_data': doctores_data,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'reportes/reporte_doctores.html', context)

@login_required
@user_passes_test(es_admin)
def reporte_pacientes(request):
    """Reporte de pacientes"""
    
    # Todos los pacientes activos
    pacientes = Paciente.objects.filter(activo=True).select_related('usuario')
    
    pacientes_data = []
    for paciente in pacientes:
        total_citas = Cita.objects.filter(paciente=paciente).count()
        citas_completadas = Cita.objects.filter(paciente=paciente, estado='completada').count()
        ultima_cita = Cita.objects.filter(paciente=paciente).order_by('-fecha').first()
        
        pacientes_data.append({
            'paciente': paciente,
            'total_citas': total_citas,
            'citas_completadas': citas_completadas,
            'ultima_cita': ultima_cita,
        })
    
    # Ordenar por total de citas
    pacientes_data.sort(key=lambda x: x['total_citas'], reverse=True)
    
    context = {
        'pacientes_data': pacientes_data,
    }
    
    return render(request, 'reportes/reporte_pacientes.html', context)

@login_required
@user_passes_test(es_admin)
def exportar_excel_citas(request):
    """Exportar citas a Excel - Funcionalidad básica"""
    messages.info(request, 'Funcionalidad de exportación a Excel en desarrollo.')
    return redirect('reporte_citas')

@login_required
@user_passes_test(es_admin)
def exportar_pdf_citas(request):
    """Exportar citas a PDF - Funcionalidad básica"""
    messages.info(request, 'Funcionalidad de exportación a PDF en desarrollo.')
    return redirect('reporte_citas')


@login_required
@user_passes_test(es_admin)
def dashboard_admin(request):
    """Dashboard principal de administración con calendario"""
    
    # Fechas para filtros
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Estadísticas generales
    total_pacientes = Paciente.objects.filter(activo=True).count()
    total_doctores = Doctor.objects.filter(activo=True).count()
    total_especialidades = Especialidad.objects.filter(activo=True).count()
    
    # Citas del mes actual
    citas_mes = Cita.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    )
    
    total_citas_mes = citas_mes.count()
    citas_hoy = Cita.objects.filter(fecha=hoy).exclude(estado='cancelada').order_by('hora_inicio')
    citas_pendientes = Cita.objects.filter(
        fecha__gte=hoy,
        estado__in=['pendiente', 'confirmada']
    ).count()
    
    # Preparar datos para el calendario (próximos 3 meses)
    from datetime import timedelta
    fecha_inicio_cal = hoy - timedelta(days=30)
    fecha_fin_cal = hoy + timedelta(days=90)
    
    citas_calendario = Cita.objects.filter(
        fecha__range=[fecha_inicio_cal, fecha_fin_cal]
    ).select_related('paciente__usuario', 'doctor__usuario').order_by('fecha', 'hora_inicio')
    
    # Estadísticas rápidas
    citas_completadas = citas_mes.filter(estado='completada').count()
    citas_canceladas = citas_mes.filter(estado='cancelada').count()
    
    context = {
        'total_pacientes': total_pacientes,
        'total_doctores': total_doctores,
        'total_especialidades': total_especialidades,
        'total_citas_mes': total_citas_mes,
        'citas_completadas': citas_completadas,
        'citas_pendientes': citas_pendientes,
        'citas_canceladas': citas_canceladas,
        'citas_hoy': citas_hoy,
        'citas_calendario': citas_calendario,
        'hoy': hoy,
    }
    
    return render(request, 'reportes/dashboard_admin_calendario.html', context)