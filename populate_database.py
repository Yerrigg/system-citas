#!/usr/bin/env python
"""
Script completo para poblar todas las tablas de la base de datos
con datos de prueba realistas

EJECUTAR: python populate_database.py
"""
import os
import django
import random
from datetime import datetime, date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from especialidades.models import Especialidad
from doctores.models import Doctor
from pacientes.models import Paciente
from horarios.models import Horario, Excepcion
from citas.models import Cita


def limpiar_datos():
    """ADVERTENCIA: Elimina todos los datos existentes"""
    print("\n" + "=" * 70)
    print("⚠️  LIMPIANDO DATOS EXISTENTES...")
    print("=" * 70)
    
    Cita.objects.all().delete()
    Excepcion.objects.all().delete()
    Horario.objects.all().delete()
    Doctor.objects.all().delete()
    Paciente.objects.all().delete()
    Especialidad.objects.all().delete()
    Usuario.objects.all().delete()
    
    print("✅ Datos eliminados\n")


def crear_especialidades():
    """Crear especialidades médicas"""
    print("=" * 70)
    print("📚 CREANDO ESPECIALIDADES")
    print("=" * 70)
    
    especialidades_data = [
        {
            'nombre': 'Medicina General',
            'descripcion': 'Atención médica general y diagnóstico de enfermedades comunes',
            'duracion_cita': 30
        },
        {
            'nombre': 'Cardiología',
            'descripcion': 'Especialidad en el diagnóstico y tratamiento de enfermedades del corazón',
            'duracion_cita': 45
        },
        {
            'nombre': 'Pediatría',
            'descripcion': 'Atención médica especializada para niños y adolescentes',
            'duracion_cita': 30
        },
        {
            'nombre': 'Dermatología',
            'descripcion': 'Diagnóstico y tratamiento de enfermedades de la piel',
            'duracion_cita': 30
        },
        {
            'nombre': 'Traumatología',
            'descripcion': 'Tratamiento de lesiones y enfermedades del sistema musculoesquelético',
            'duracion_cita': 40
        },
        {
            'nombre': 'Ginecología',
            'descripcion': 'Atención especializada en salud femenina',
            'duracion_cita': 40
        },
        {
            'nombre': 'Oftalmología',
            'descripcion': 'Diagnóstico y tratamiento de enfermedades de los ojos',
            'duracion_cita': 35
        },
        {
            'nombre': 'Psiquiatría',
            'descripcion': 'Diagnóstico y tratamiento de trastornos mentales',
            'duracion_cita': 60
        },
        {
            'nombre': 'Neurología',
            'descripcion': 'Tratamiento de enfermedades del sistema nervioso',
            'duracion_cita': 45
        },
        {
            'nombre': 'Odontología',
            'descripcion': 'Cuidado de la salud bucal y dental',
            'duracion_cita': 30
        }
    ]
    
    especialidades = []
    for esp_data in especialidades_data:
        especialidad, created = Especialidad.objects.get_or_create(
            nombre=esp_data['nombre'],
            defaults=esp_data
        )
        especialidades.append(especialidad)
        status = "✅ Creada" if created else "ℹ️  Ya existe"
        print(f"{status}: {especialidad.nombre}")
    
    print(f"\n✅ Total: {len(especialidades)} especialidades\n")
    return especialidades


def crear_usuarios_admin():
    """Crear usuarios administradores"""
    print("=" * 70)
    print("👤 CREANDO ADMINISTRADORES")
    print("=" * 70)
    
    admins_data = [
        {
            'username': 'admin',
            'email': 'admin@systemcitas.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'rol': 'admin',
            'telefono': '999888777',
            'is_superuser': True,
            'is_staff': True
        },
        {
            'username': 'admin2',
            'email': 'admin2@systemcitas.com',
            'password': 'admin123',
            'first_name': 'Carlos',
            'last_name': 'Administrador',
            'rol': 'admin',
            'telefono': '999888778',
            'is_staff': True
        }
    ]
    
    admins = []
    for admin_data in admins_data:
        if not Usuario.objects.filter(username=admin_data['username']).exists():
            is_superuser = admin_data.pop('is_superuser', False)
            is_staff = admin_data.pop('is_staff', False)
            password = admin_data.pop('password')
            
            if is_superuser:
                user = Usuario.objects.create_superuser(password=password, **admin_data)
            else:
                user = Usuario.objects.create_user(password=password, **admin_data)
                user.is_staff = is_staff
                user.save()
            
            admins.append(user)
            print(f"✅ Creado: {user.username} ({user.email})")
        else:
            print(f"ℹ️  Ya existe: {admin_data['username']}")
    
    print(f"\n✅ Total: {len(admins)} administradores\n")
    return admins


def crear_doctores(especialidades):
    """Crear doctores con sus usuarios"""
    print("=" * 70)
    print("👨‍⚕️ CREANDO DOCTORES")
    print("=" * 70)
    
    doctores_data = [
        {
            'username': 'doctor1',
            'password': 'doctor123',
            'first_name': 'Juan',
            'last_name': 'Pérez García',
            'email': 'juan.perez@hospital.com',
            'telefono': '987654321',
            'fecha_nacimiento': date(1980, 5, 15),
            'licencia_medica': 'CMP-12345',
            'biografia': 'Médico general con 15 años de experiencia',
            'anos_experiencia': 15,
            'especialidades': ['Medicina General', 'Cardiología']
        },
        {
            'username': 'doctor2',
            'password': 'doctor123',
            'first_name': 'María',
            'last_name': 'González López',
            'email': 'maria.gonzalez@hospital.com',
            'telefono': '987654322',
            'fecha_nacimiento': date(1985, 8, 20),
            'licencia_medica': 'CMP-23456',
            'biografia': 'Especialista en pediatría con amplia experiencia',
            'anos_experiencia': 10,
            'especialidades': ['Pediatría']
        },
        {
            'username': 'doctor3',
            'password': 'doctor123',
            'first_name': 'Carlos',
            'last_name': 'Ramírez Silva',
            'email': 'carlos.ramirez@hospital.com',
            'telefono': '987654323',
            'fecha_nacimiento': date(1978, 3, 10),
            'licencia_medica': 'CMP-34567',
            'biografia': 'Cardiólogo reconocido internacionalmente',
            'anos_experiencia': 18,
            'especialidades': ['Cardiología']
        },
        {
            'username': 'doctor4',
            'password': 'doctor123',
            'first_name': 'Ana',
            'last_name': 'Martínez Torres',
            'email': 'ana.martinez@hospital.com',
            'telefono': '987654324',
            'fecha_nacimiento': date(1988, 11, 5),
            'licencia_medica': 'CMP-45678',
            'biografia': 'Dermatóloga con especialización en cirugía estética',
            'anos_experiencia': 8,
            'especialidades': ['Dermatología']
        },
        {
            'username': 'doctor5',
            'password': 'doctor123',
            'first_name': 'Luis',
            'last_name': 'Fernández Ruiz',
            'email': 'luis.fernandez@hospital.com',
            'telefono': '987654325',
            'fecha_nacimiento': date(1982, 7, 25),
            'licencia_medica': 'CMP-56789',
            'biografia': 'Traumatólogo especialista en lesiones deportivas',
            'anos_experiencia': 12,
            'especialidades': ['Traumatología']
        },
        {
            'username': 'doctor6',
            'password': 'doctor123',
            'first_name': 'Patricia',
            'last_name': 'Sánchez Vega',
            'email': 'patricia.sanchez@hospital.com',
            'telefono': '987654326',
            'fecha_nacimiento': date(1986, 12, 18),
            'licencia_medica': 'CMP-67890',
            'biografia': 'Ginecóloga especializada en embarazos de alto riesgo',
            'anos_experiencia': 11,
            'especialidades': ['Ginecología']
        },
        {
            'username': 'doctor7',
            'password': 'doctor123',
            'first_name': 'Roberto',
            'last_name': 'Díaz Castro',
            'email': 'roberto.diaz@hospital.com',
            'telefono': '987654327',
            'fecha_nacimiento': date(1984, 4, 8),
            'licencia_medica': 'CMP-78901',
            'biografia': 'Oftalmólogo con subespecialidad en cirugía refractiva',
            'anos_experiencia': 13,
            'especialidades': ['Oftalmología']
        },
        {
            'username': 'doctor8',
            'password': 'doctor123',
            'first_name': 'Laura',
            'last_name': 'Morales Jiménez',
            'email': 'laura.morales@hospital.com',
            'telefono': '987654328',
            'fecha_nacimiento': date(1990, 9, 22),
            'licencia_medica': 'CMP-89012',
            'biografia': 'Psiquiatra especializada en terapia cognitivo-conductual',
            'anos_experiencia': 7,
            'especialidades': ['Psiquiatría']
        }
    ]
    
    doctores = []
    for doc_data in doctores_data:
        if not Usuario.objects.filter(username=doc_data['username']).exists():
            # Extraer datos específicos del doctor
            licencia = doc_data.pop('licencia_medica')
            biografia = doc_data.pop('biografia')
            anos_exp = doc_data.pop('anos_experiencia')
            especialidades_nombres = doc_data.pop('especialidades')
            password = doc_data.pop('password')
            
            # Crear usuario
            usuario = Usuario.objects.create_user(
                password=password,
                rol='doctor',
                **doc_data
            )
            
            # Crear doctor
            doctor = Doctor.objects.create(
                usuario=usuario,
                licencia_medica=licencia,
                biografia=biografia,
                anos_experiencia=anos_exp
            )
            
            # Asignar especialidades
            for esp_nombre in especialidades_nombres:
                especialidad = Especialidad.objects.get(nombre=esp_nombre)
                doctor.especialidades.add(especialidad)
            
            doctores.append(doctor)
            print(f"✅ Creado: Dr. {usuario.get_full_name()} - {', '.join(especialidades_nombres)}")
        else:
            print(f"ℹ️  Ya existe: {doc_data['username']}")
    
    print(f"\n✅ Total: {len(doctores)} doctores\n")
    return doctores


def crear_pacientes():
    """Crear pacientes con sus usuarios"""
    print("=" * 70)
    print("🧑‍💼 CREANDO PACIENTES")
    print("=" * 70)
    
    pacientes_data = [
        {
            'username': 'paciente1',
            'password': 'paciente123',
            'first_name': 'Pedro',
            'last_name': 'López Morales',
            'email': 'pedro.lopez@mail.com',
            'telefono': '965432101',
            'fecha_nacimiento': date(1990, 3, 15),
            'dni': '12345678',
            'direccion': 'Av. Los Pinos 123, Lima',
            'grupo_sanguineo': 'O+',
            'alergias': 'Penicilina',
            'contacto_emergencia': 'Rosa López (Madre)',
            'telefono_emergencia': '965432100'
        },
        {
            'username': 'paciente2',
            'password': 'paciente123',
            'first_name': 'María',
            'last_name': 'Rodríguez Silva',
            'email': 'maria.rodriguez@mail.com',
            'telefono': '965432102',
            'fecha_nacimiento': date(1985, 7, 20),
            'dni': '23456789',
            'direccion': 'Jr. Las Flores 456, Lima',
            'grupo_sanguineo': 'A+',
            'alergias': 'Ninguna',
            'contacto_emergencia': 'Juan Rodríguez (Esposo)',
            'telefono_emergencia': '965432103'
        },
        {
            'username': 'paciente3',
            'password': 'paciente123',
            'first_name': 'Carlos',
            'last_name': 'García Vega',
            'email': 'carlos.garcia@mail.com',
            'telefono': '965432104',
            'fecha_nacimiento': date(1992, 11, 5),
            'dni': '34567890',
            'direccion': 'Calle Los Olivos 789, Lima',
            'grupo_sanguineo': 'B+',
            'alergias': 'Polen, Ácaros',
            'contacto_emergencia': 'Ana García (Hermana)',
            'telefono_emergencia': '965432105'
        },
        {
            'username': 'paciente4',
            'password': 'paciente123',
            'first_name': 'Ana',
            'last_name': 'Martínez Castro',
            'email': 'ana.martinez@mail.com',
            'telefono': '965432106',
            'fecha_nacimiento': date(1988, 4, 12),
            'dni': '45678901',
            'direccion': 'Av. La Marina 321, Lima',
            'grupo_sanguineo': 'AB+',
            'alergias': 'Lactosa',
            'contacto_emergencia': 'Luis Martínez (Padre)',
            'telefono_emergencia': '965432107'
        },
        {
            'username': 'paciente5',
            'password': 'paciente123',
            'first_name': 'Jorge',
            'last_name': 'Sánchez Ruiz',
            'email': 'jorge.sanchez@mail.com',
            'telefono': '965432108',
            'fecha_nacimiento': date(1995, 9, 8),
            'dni': '56789012',
            'direccion': 'Jr. Los Rosales 654, Lima',
            'grupo_sanguineo': 'O-',
            'alergias': 'Mariscos',
            'contacto_emergencia': 'Carmen Sánchez (Madre)',
            'telefono_emergencia': '965432109'
        },
        {
            'username': 'paciente6',
            'password': 'paciente123',
            'first_name': 'Laura',
            'last_name': 'Fernández Torres',
            'email': 'laura.fernandez@mail.com',
            'telefono': '965432110',
            'fecha_nacimiento': date(1993, 12, 25),
            'dni': '67890123',
            'direccion': 'Calle Las Palmeras 987, Lima',
            'grupo_sanguineo': 'A-',
            'alergias': 'Ninguna',
            'contacto_emergencia': 'Roberto Fernández (Esposo)',
            'telefono_emergencia': '965432111'
        },
        {
            'username': 'paciente7',
            'password': 'paciente123',
            'first_name': 'Diego',
            'last_name': 'Ramírez López',
            'email': 'diego.ramirez@mail.com',
            'telefono': '965432112',
            'fecha_nacimiento': date(1987, 6, 18),
            'dni': '78901234',
            'direccion': 'Av. Los Heroes 147, Lima',
            'grupo_sanguineo': 'B-',
            'alergias': 'Aspirina',
            'contacto_emergencia': 'Patricia Ramírez (Hermana)',
            'telefono_emergencia': '965432113'
        },
        {
            'username': 'paciente8',
            'password': 'paciente123',
            'first_name': 'Sofía',
            'last_name': 'Díaz Morales',
            'email': 'sofia.diaz@mail.com',
            'telefono': '965432114',
            'fecha_nacimiento': date(1991, 2, 14),
            'dni': '89012345',
            'direccion': 'Jr. Las Camelias 258, Lima',
            'grupo_sanguineo': 'AB-',
            'alergias': 'Ninguna',
            'contacto_emergencia': 'Miguel Díaz (Padre)',
            'telefono_emergencia': '965432115'
        },
        {
            'username': 'paciente9',
            'password': 'paciente123',
            'first_name': 'Roberto',
            'last_name': 'Torres Silva',
            'email': 'roberto.torres@mail.com',
            'telefono': '965432116',
            'fecha_nacimiento': date(1989, 10, 30),
            'dni': '90123456',
            'direccion': 'Calle Los Jazmines 369, Lima',
            'grupo_sanguineo': 'O+',
            'alergias': 'Frutos secos',
            'contacto_emergencia': 'Elena Torres (Esposa)',
            'telefono_emergencia': '965432117'
        },
        {
            'username': 'paciente10',
            'password': 'paciente123',
            'first_name': 'Valeria',
            'last_name': 'Castro Vega',
            'email': 'valeria.castro@mail.com',
            'telefono': '965432118',
            'fecha_nacimiento': date(1994, 5, 7),
            'dni': '01234567',
            'direccion': 'Av. Los Sauces 741, Lima',
            'grupo_sanguineo': 'A+',
            'alergias': 'Yodo',
            'contacto_emergencia': 'Fernando Castro (Hermano)',
            'telefono_emergencia': '965432119'
        }
    ]
    
    pacientes = []
    for pac_data in pacientes_data:
        if not Usuario.objects.filter(username=pac_data['username']).exists():
            # Extraer datos específicos del paciente
            dni = pac_data.pop('dni')
            direccion = pac_data.pop('direccion')
            grupo_sanguineo = pac_data.pop('grupo_sanguineo')
            alergias = pac_data.pop('alergias')
            contacto_emergencia = pac_data.pop('contacto_emergencia')
            telefono_emergencia = pac_data.pop('telefono_emergencia')
            password = pac_data.pop('password')
            
            # Crear usuario
            usuario = Usuario.objects.create_user(
                password=password,
                rol='paciente',
                **pac_data
            )
            
            # Crear paciente
            paciente = Paciente.objects.create(
                usuario=usuario,
                dni=dni,
                direccion=direccion,
                grupo_sanguineo=grupo_sanguineo,
                alergias=alergias,
                contacto_emergencia=contacto_emergencia,
                telefono_emergencia=telefono_emergencia
            )
            
            pacientes.append(paciente)
            print(f"✅ Creado: {usuario.get_full_name()} - DNI: {dni}")
        else:
            print(f"ℹ️  Ya existe: {pac_data['username']}")
    
    print(f"\n✅ Total: {len(pacientes)} pacientes\n")
    return pacientes


def crear_horarios(doctores):
    """Crear horarios de trabajo para los doctores"""
    print("=" * 70)
    print("🕐 CREANDO HORARIOS")
    print("=" * 70)
    
    horarios_creados = 0
    
    for doctor in doctores:
        # Horario típico: Lunes a Viernes 8:00-17:00
        for dia in range(5):  # 0=Lunes, 4=Viernes
            # Turno mañana
            Horario.objects.get_or_create(
                doctor=doctor,
                dia_semana=dia,
                hora_inicio=time(8, 0),
                hora_fin=time(13, 0)
            )
            horarios_creados += 1
            
            # Turno tarde
            Horario.objects.get_or_create(
                doctor=doctor,
                dia_semana=dia,
                hora_inicio=time(14, 0),
                hora_fin=time(17, 0)
            )
            horarios_creados += 1
        
        # Algunos doctores trabajan sábados
        if random.choice([True, False]):
            Horario.objects.get_or_create(
                doctor=doctor,
                dia_semana=5,  # Sábado
                hora_inicio=time(9, 0),
                hora_fin=time(13, 0)
            )
            horarios_creados += 1
        
        print(f"✅ Horarios creados para: Dr. {doctor.usuario.get_full_name()}")
    
    print(f"\n✅ Total: {horarios_creados} horarios\n")


def crear_excepciones(doctores):
    """Crear excepciones de horario (vacaciones, etc.)"""
    print("=" * 70)
    print("🚫 CREANDO EXCEPCIONES DE HORARIO")
    print("=" * 70)
    
    excepciones_creadas = 0
    
    # Algunos doctores tendrán vacaciones en el futuro
    for doctor in random.sample(list(doctores), 3):
        fecha_inicio = date.today() + timedelta(days=random.randint(30, 60))
        fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 14))
        
        Excepcion.objects.get_or_create(
            doctor=doctor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            motivo='vacaciones',
            descripcion='Vacaciones programadas'
        )
        excepciones_creadas += 1
        print(f"✅ Vacaciones: Dr. {doctor.usuario.get_full_name()} ({fecha_inicio} - {fecha_fin})")
    
    print(f"\n✅ Total: {excepciones_creadas} excepciones\n")


def crear_citas(doctores, pacientes):
    """Crear citas de ejemplo"""
    print("=" * 70)
    print("📅 CREANDO CITAS")
    print("=" * 70)
    
    estados = ['pendiente', 'confirmada', 'completada', 'cancelada']
    tipos = ['primera_vez', 'control', 'urgencia']
    motivos = [
        'Consulta general',
        'Control de rutina',
        'Dolor de cabeza persistente',
        'Chequeo anual',
        'Seguimiento de tratamiento',
        'Dolor abdominal',
        'Tos y gripe',
        'Control post-operatorio',
        'Renovación de receta médica',
        'Evaluación pre-quirúrgica'
    ]
    
    citas_creadas = 0
    
    # Crear citas en diferentes fechas
    for dias in range(-30, 60):  # Citas desde hace 30 días hasta 60 días en el futuro
        fecha = date.today() + timedelta(days=dias)
        
        # Saltar domingos
        if fecha.weekday() == 6:
            continue
        
        # 2-5 citas por día
        num_citas = random.randint(2, 5)
        
        for _ in range(num_citas):
            doctor = random.choice(doctores)
            paciente = random.choice(pacientes)
            
            # Horarios posibles: 8:00, 9:00, 10:00, 11:00, 14:00, 15:00, 16:00
            horas_posibles = [
                time(8, 0), time(9, 0), time(10, 0), time(11, 0),
                time(14, 0), time(15, 0), time(16, 0)
            ]
            hora_inicio = random.choice(horas_posibles)
            hora_fin = (datetime.combine(date.today(), hora_inicio) + 
                       timedelta(minutes=random.choice([30, 45, 60]))).time()
            
            # Estado según la fecha
            if fecha < date.today():
                estado = random.choice(['completada', 'no_asistio', 'cancelada'])
            elif fecha == date.today():
                estado = random.choice(['pendiente', 'confirmada', 'en_curso'])
            else:
                estado = random.choice(['pendiente', 'confirmada'])
            
            tipo = random.choice(tipos)
            motivo = random.choice(motivos)
            
            try:
                cita = Cita.objects.create(
                    paciente=paciente,
                    doctor=doctor,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    tipo=tipo,
                    estado=estado,
                    motivo=motivo
                )
                
                # Agregar notas para citas completadas
                if estado == 'completada':
                    cita.notas = f"Paciente atendido sin complicaciones. {motivo}."
                    cita.diagnostico = random.choice([
                        'Sin patología aparente',
                        'Hipertensión leve',
                        'Infección respiratoria alta',
                        'Gastritis crónica',
                        'Ansiedad leve'
                    ])
                    cita.tratamiento = random.choice([
                        'Reposo y analgésicos',
                        'Control en 1 mes',
                        'Antibióticos por 7 días',
                        'Dieta blanda y antácidos',
                        'Terapia psicológica'
                    ])
                    cita.save()
                
                citas_creadas += 1
                
                if citas_creadas % 10 == 0:
                    print(f"✅ Creadas {citas_creadas} citas...")
            
            except Exception as e:
                # Ignorar conflictos de horario (citas duplicadas)
                pass
    
    print(f"\n✅ Total: {citas_creadas} citas\n")


def crear_recepcionistas():
    """Crear usuarios recepcionistas"""
    print("=" * 70)
    print("📋 CREANDO RECEPCIONISTAS")
    print("=" * 70)
    
    recepcionistas_data = [
        {
            'username': 'recepcionista1',
            'password': 'recep123',
            'first_name': 'Luis',
            'last_name': 'Rodríguez Pérez',
            'email': 'luis.rodriguez@hospital.com',
            'rol': 'recepcionista',
            'telefono': '945678901'
        },
        {
            'username': 'recepcionista2',
            'password': 'recep123',
            'first_name': 'Carmen',
            'last_name': 'Flores Sánchez',
            'email': 'carmen.flores@hospital.com',
            'rol': 'recepcionista',
            'telefono': '945678902'
        }
    ]
    
    recepcionistas = []
    for recep_data in recepcionistas_data:
        if not Usuario.objects.filter(username=recep_data['username']).exists():
            password = recep_data.pop('password')
            usuario = Usuario.objects.create_user(password=password, **recep_data)
            recepcionistas.append(usuario)
            print(f"✅ Creado: {usuario.get_full_name()}")
        else:
            print(f"ℹ️  Ya existe: {recep_data['username']}")
    
    print(f"\n✅ Total: {len(recepcionistas)} recepcionistas\n")
    return recepcionistas


def mostrar_resumen():
    """Mostrar resumen de datos creados"""
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70)
    
    print(f"\n👥 USUARIOS:")
    print(f"   - Administradores: {Usuario.objects.filter(rol='admin').count()}")
    print(f"   - Doctores: {Usuario.objects.filter(rol='doctor').count()}")
    print(f"   - Pacientes: {Usuario.objects.filter(rol='paciente').count()}")
    print(f"   - Recepcionistas: {Usuario.objects.filter(rol='recepcionista').count()}")
    print(f"   📌 TOTAL: {Usuario.objects.count()} usuarios")
    
    print(f"\n📚 ESPECIALIDADES: {Especialidad.objects.count()}")
    print(f"👨‍⚕️ DOCTORES: {Doctor.objects.count()}")
    print(f"🧑‍💼 PACIENTES: {Paciente.objects.count()}")
    print(f"🕐 HORARIOS: {Horario.objects.count()}")
    print(f"🚫 EXCEPCIONES: {Excepcion.objects.count()}")
    print(f"📅 CITAS: {Cita.objects.count()}")
    
    print(f"\n📈 ESTADÍSTICAS DE CITAS:")
    print(f"   - Pendientes: {Cita.objects.filter(estado='pendiente').count()}")
    print(f"   - Confirmadas: {Cita.objects.filter(estado='confirmada').count()}")
    print(f"   - Completadas: {Cita.objects.filter(estado='completada').count()}")
    print(f"   - Canceladas: {Cita.objects.filter(estado='cancelada').count()}")
    
    print("\n" + "=" * 70)
    print("🔑 CREDENCIALES DE ACCESO")
    print("=" * 70)
    
    print("\n🔐 ADMINISTRADORES:")
    print("   username: admin / password: admin123")
    print("   username: admin2 / password: admin123")
    
    print("\n👨‍⚕️ DOCTORES (todos con password: doctor123):")
    for doctor in Doctor.objects.all()[:5]:
        print(f"   username: {doctor.usuario.username} - Dr. {doctor.usuario.get_full_name()}")
    
    print("\n🧑‍💼 PACIENTES (todos con password: paciente123):")
    for paciente in Paciente.objects.all()[:5]:
        print(f"   username: {paciente.usuario.username} - {paciente.usuario.get_full_name()}")
    
    print("\n📋 RECEPCIONISTAS (todos con password: recep123):")
    for recep in Usuario.objects.filter(rol='recepcionista'):
        print(f"   username: {recep.username} - {recep.get_full_name()}")
    
    print("\n" + "=" * 70)


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🏥 SCRIPT DE POBLACIÓN DE BASE DE DATOS")
    print("   Sistema de Citas Médicas")
    print("=" * 70)
    
    respuesta = input("\n⚠️  ¿Desea ELIMINAR todos los datos existentes? (s/n): ")
    
    if respuesta.lower() == 's':
        limpiar_datos()
    
    print("\n🚀 Iniciando población de base de datos...\n")
    
    try:
        # 1. Crear especialidades
        especialidades = crear_especialidades()
        
        # 2. Crear administradores
        admins = crear_usuarios_admin()
        
        # 3. Crear recepcionistas
        recepcionistas = crear_recepcionistas()
        
        # 4. Crear doctores
        doctores = crear_doctores(especialidades)
        
        # 5. Crear pacientes
        pacientes = crear_pacientes()
        
        # 6. Crear horarios para doctores
        crear_horarios(doctores)
        
        # 7. Crear excepciones de horario
        crear_excepciones(doctores)
        
        # 8. Crear citas
        crear_citas(doctores, pacientes)
        
        # 9. Mostrar resumen
        mostrar_resumen()
        
        print("\n✅ ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
