from django.urls import path
from . import views

urlpatterns = [
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('doctores/especialidad/<int:especialidad_id>/', views.lista_doctores, name='lista_doctores_especialidad'),
    path('doctor/<int:doctor_id>/disponibilidad/', views.disponibilidad_doctor, name='disponibilidad_doctor'),
    path('doctor/<int:doctor_id>/agendar/', views.agendar_cita, name='agendar_cita'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('cita/<int:cita_id>/', views.detalle_cita, name='detalle_cita'),
    path('cita/<int:cita_id>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
]