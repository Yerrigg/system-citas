from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_doctor, name='dashboard_doctor'),
    path('agenda/', views.agenda_doctor, name='agenda_doctor'),
    path('cita/<int:cita_id>/atender/', views.atender_cita, name='atender_cita'),
    path('cita/<int:cita_id>/confirmar/', views.confirmar_cita, name='confirmar_cita'),
    path('cita/<int:cita_id>/no-asistio/', views.marcar_no_asistio, name='marcar_no_asistio'),
    path('pacientes/', views.mis_pacientes, name='mis_pacientes'),
    path('paciente/<int:paciente_id>/historial/', views.historial_paciente, name='historial_paciente'),
    path('horarios/', views.gestionar_horarios, name='gestionar_horarios'),
    path('horario/<int:horario_id>/eliminar/', views.eliminar_horario, name='eliminar_horario'),
    path('excepcion/agregar/', views.agregar_excepcion, name='agregar_excepcion'),
    path('buscar/', views.buscar_doctores, name='buscar_doctores'),
]