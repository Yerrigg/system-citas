from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'dni', 'grupo_sanguineo', 'activo', 'created_at']
    list_filter = ['activo', 'grupo_sanguineo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'dni']
    
    def get_nombre(self, obj):
        return obj.usuario.get_full_name()
    get_nombre.short_description = 'Nombre'