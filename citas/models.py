from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from pacientes.models import Paciente
from doctores.models import Doctor

class Cita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    TIPOS = [
        ('primera_vez', 'Primera Vez'),
        ('control', 'Control'),
        ('urgencia', 'Urgencia'),
        ('telemedicina', 'Telemedicina'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='primera_vez')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    motivo = models.TextField()
    notas = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha', '-hora_inicio']
        unique_together = ['doctor', 'fecha', 'hora_inicio']

    def __str__(self):
        return f"Cita: {self.paciente.usuario.get_full_name()} con {self.doctor} - {self.fecha} {self.hora_inicio}"
    
    def clean(self):
        """Validaciones personalizadas"""
        
        # 1. Validar que la fecha no sea en el pasado
        if self.fecha and self.fecha < timezone.now().date():
            raise ValidationError({
                'fecha': 'No se pueden agendar citas en fechas pasadas.'
            })
        
        # 2. Validar que la hora de fin sea mayor a la hora de inicio
        if self.hora_inicio and self.hora_fin:
            if self.hora_fin <= self.hora_inicio:
                raise ValidationError({
                    'hora_fin': 'La hora de fin debe ser posterior a la hora de inicio.'
                })
        
        # 3. Validar que no haya conflicto de horarios con el mismo doctor
        if self.doctor and self.fecha and self.hora_inicio and self.hora_fin:
            citas_conflicto = Cita.objects.filter(
                doctor=self.doctor,
                fecha=self.fecha,
                estado__in=['pendiente', 'confirmada', 'en_curso']
            ).exclude(pk=self.pk)  # Excluir la cita actual si es edición
            
            for cita in citas_conflicto:
                # Verificar solapamiento de horarios
                if (self.hora_inicio < cita.hora_fin and self.hora_fin > cita.hora_inicio):
                    raise ValidationError({
                        'hora_inicio': f'Ya existe una cita para este doctor el {self.fecha} de {cita.hora_inicio.strftime("%H:%M")} a {cita.hora_fin.strftime("%H:%M")}.'
                    })
        
        # 4. Validar que la cita sea en horario laboral del doctor
        if self.doctor and self.fecha and self.hora_inicio:
            dia_semana = self.fecha.weekday()  # 0=Lunes, 6=Domingo
            
            from horarios.models import Horario, Excepcion
            
            # Verificar si el doctor trabaja ese día
            horarios_dia = Horario.objects.filter(
                doctor=self.doctor,
                dia_semana=dia_semana,
                activo=True
            )
            
            if not horarios_dia.exists():
                dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
                raise ValidationError({
                    'fecha': f'El doctor no trabaja los {dias[dia_semana]}.'
                })
            
            # Verificar que la hora esté dentro del horario laboral
            horario_valido = False
            for horario in horarios_dia:
                if horario.hora_inicio <= self.hora_inicio < horario.hora_fin:
                    horario_valido = True
                    break
            
            if not horario_valido:
                raise ValidationError({
                    'hora_inicio': 'La hora seleccionada está fuera del horario laboral del doctor.'
                })
            
            # Verificar excepciones (vacaciones, bloqueos)
            excepciones = Excepcion.objects.filter(
                doctor=self.doctor,
                fecha_inicio__lte=self.fecha,
                fecha_fin__gte=self.fecha
            )
            
            if excepciones.exists():
                excepcion = excepciones.first()
                raise ValidationError({
                    'fecha': f'El doctor no está disponible en esta fecha ({excepcion.get_motivo_display()}).'
                })
    
    def save(self, *args, **kwargs):
        """Ejecutar validaciones antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)