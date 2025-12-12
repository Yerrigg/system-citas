from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['get_paciente', 'get_doctor', 'fecha', 'hora_inicio', 'tipo', 'estado']
    list_filter = ['estado', 'tipo', 'fecha']
    search_fields = [
        'paciente__usuario__first_name', 
        'paciente__usuario__last_name',
        'doctor__usuario__first_name',
        'doctor__usuario__last_name'
    ]
    date_hierarchy = 'fecha'
    
    def get_paciente(self, obj):
        return obj.paciente.usuario.get_full_name()
    get_paciente.short_description = 'Paciente'
    
    def get_doctor(self, obj):
        return obj.doctor.usuario.get_full_name()
    get_doctor.short_description = 'Doctor'