from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('paciente', 'Paciente'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='paciente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"