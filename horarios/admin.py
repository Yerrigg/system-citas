from django.contrib import admin
from .models import Horario, Excepcion

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'get_dia', 'hora_inicio', 'hora_fin', 'activo']
    list_filter = ['dia_semana', 'activo']
    search_fields = ['doctor__usuario__first_name', 'doctor__usuario__last_name']
    
    def get_dia(self, obj):
        return obj.get_dia_semana_display()
    get_dia.short_description = 'Día'

@admin.register(Excepcion)
class ExcepcionAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'motivo', 'fecha_inicio', 'fecha_fin']
    list_filter = ['motivo']
    search_fields = ['doctor__usuario__first_name', 'doctor__usuario__last_name']