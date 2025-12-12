from django.contrib import admin
from .models import Especialidad

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion_cita', 'activo', 'created_at']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']