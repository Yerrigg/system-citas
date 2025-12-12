from django.db import models
from usuarios.models import Usuario
from especialidades.models import Especialidad

class Doctor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='doctor')
    especialidades = models.ManyToManyField(Especialidad, related_name='doctores')
    licencia_medica = models.CharField(max_length=50, unique=True)
    biografia = models.TextField(blank=True, null=True)
    anos_experiencia = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()}"