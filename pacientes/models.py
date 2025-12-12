from django.db import models
from usuarios.models import Usuario

class Paciente(models.Model):
    GRUPOS_SANGUINEOS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='paciente')
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPOS_SANGUINEOS, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True, null=True)
    telefono_emergencia = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.dni}"