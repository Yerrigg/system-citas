from django.db import models
from doctores.models import Doctor

class Horario(models.Model):
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        unique_together = ['doctor', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f"{self.doctor} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class Excepcion(models.Model):
    TIPOS = [
        ('vacaciones', 'Vacaciones'),
        ('capacitacion', 'Capacitación'),
        ('personal', 'Personal'),
        ('emergencia', 'Emergencia'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='excepciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Excepción de Horario"
        verbose_name_plural = "Excepciones de Horario"

    def __str__(self):
        return f"{self.doctor} - {self.get_motivo_display()} ({self.fecha_inicio} - {self.fecha_fin})"