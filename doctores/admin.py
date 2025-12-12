from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'licencia_medica', 'anos_experiencia', 'activo']
    list_filter = ['activo', 'especialidades']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'licencia_medica']
    filter_horizontal = ['especialidades']
    
    def get_nombre(self, obj):
        return obj.usuario.get_full_name()
    get_nombre.short_description = 'Nombre'