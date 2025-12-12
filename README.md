# 🏥 System Citas - Sistema de Gestión de Citas Médicas

Sistema web desarrollado en Django para la gestión integral de citas médicas con calendario interactivo, reportes avanzados y gestión completa de usuarios.

---

## 📋 Características Principales

### 👤 Para Pacientes
- ✅ **Registro e inicio de sesión** seguro con validaciones
- ✅ **Búsqueda avanzada de doctores** por nombre, especialidad o licencia médica
- ✅ **Calendario de disponibilidad** de doctores en tiempo real
- ✅ **Agendar citas médicas** con validación de horarios
- ✅ **Historial completo de citas** con filtros por estado
- ✅ **Cancelar citas** con confirmación
- ✅ **Ver detalles de consultas** (diagnóstico, tratamiento, notas médicas)
- ✅ **Perfil editable** con información médica (alergias, grupo sanguíneo, contacto de emergencia)
- ✅ **Cambiar contraseña** de forma segura

### 👨‍⚕️ Para Doctores
- ✅ **Dashboard personalizado** con estadísticas en tiempo real:
  - Citas de hoy, completadas, pendientes
  - Total de pacientes atendidos
  - Gráficos de rendimiento mensual
- ✅ **Agenda completa** con filtros por fecha y estado
- ✅ **Gestión de horarios de atención** (días y horas laborables)
- ✅ **Atender pacientes** con registro completo:
  - Diagnóstico médico
  - Tratamiento y medicamentos
  - Observaciones generales
- ✅ **Historial médico completo** de cada paciente
- ✅ **Confirmar/rechazar citas** con un clic
- ✅ **Gestionar excepciones** (vacaciones, bloqueos de agenda)
- ✅ **Ver próximas citas** (7 días)
- ✅ **Lista de todos mis pacientes** con estadísticas

### 🔧 Para Administradores
- ✅ **Dashboard administrativo avanzado** con:
  - **Calendario interactivo FullCalendar** con todas las citas del sistema
  - Vista Mes/Semana/Día navegable
  - Colores por estado de cita (Pendiente/Confirmada/Completada/Cancelada)
  - Modal informativo al hacer clic en citas
  - **Citas de hoy** en panel lateral
  - **4 Tarjetas de estadísticas**: Total pacientes, doctores, citas pendientes, citas del mes
- ✅ **Reportes detallados** con filtros avanzados:
  - **Reporte de Citas**: Filtros por estado, especialidad, doctor, rango de fechas
  - **Reporte de Doctores**: Estadísticas individuales de cada doctor
  - **Reporte de Pacientes**: Información completa de todos los pacientes
- ✅ **Exportación a Excel** de todos los reportes
- ✅ **Gestión completa** del sistema desde Django Admin
- ✅ **Accesos rápidos** a todas las secciones

---

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.11+** - Lenguaje de programación
- **Django 5.0** - Framework web
- **PostgreSQL** - Base de datos relacional
- **Django ORM** - Mapeo objeto-relacional

### Frontend
- **HTML5 / CSS3** - Estructura y estilos
- **Bootstrap 5.3** - Framework CSS responsive
- **FullCalendar 6.1.10** - Calendario interactivo
- **Font Awesome 6** - Iconos
- **JavaScript ES6** - Interactividad

### Librerías Adicionales
- **openpyxl** - Exportación a Excel
- **Pillow** - Manejo de imágenes
- **python-dateutil** - Manejo de fechas

---

## 📦 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- PostgreSQL 14 o superior
- pip (gestor de paquetes de Python)
- Git

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/system-citas.git
cd system-citas
```

### 2️⃣ Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar base de datos

**Crear base de datos en PostgreSQL:**
```sql
CREATE DATABASE system_citas
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    CONNECTION LIMIT = -1;
```

**Configurar credenciales en `config/settings.py`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'system_citas',
        'USER': 'postgres',
        'PASSWORD': 'tu_password_aqui',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5️⃣ Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Crear superusuario (Administrador)
```bash
python manage.py createsuperuser
```
Ingresa:
- Username: `admin`
- Email: `admin@systemcitas.com`
- Password: `admin123` (o la que prefieras)

### 7️⃣ Crear datos iniciales (Opcional)

**Crear especialidades y doctores desde el Admin Django:**
1. Ejecuta el servidor: `python manage.py runserver`
2. Ve a: `http://127.0.0.1:8000/admin/`
3. Crea especialidades (Cardiología, Pediatría, etc.)
4. Crea usuarios tipo "Doctor" y sus perfiles

### 8️⃣ Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Acceder a: **http://127.0.0.1:8000**

---

## 📊 Estructura del Proyecto
```
system-citas/
├── config/                      # Configuración principal de Django
│   ├── settings.py              # Configuración del proyecto
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuración WSGI
│
├── usuarios/                    # App de usuarios y autenticación
│   ├── models.py                # Modelo Usuario personalizado
│   ├── views.py                 # Login, registro, logout, perfil
│   └── urls.py                  # URLs de usuarios
│
├── doctores/                    # App de doctores
│   ├── models.py                # Modelo Doctor
│   ├── views.py                 # Dashboard doctor, agenda, atender pacientes
│   └── templates/doctores/      # Templates de doctores
│
├── pacientes/                   # App de pacientes
│   ├── models.py                # Modelo Paciente
│   └── views.py                 # Gestión de pacientes
│
├── citas/                       # App de citas (CORE)
│   ├── models.py                # Modelo Cita (estados, tipos)
│   ├── views.py                 # Agendar, cancelar, ver citas
│   └── templates/citas/         # Templates de citas
│
├── especialidades/              # App de especialidades médicas
│   ├── models.py                # Modelo Especialidad
│   └── views.py                 # CRUD de especialidades
│
├── horarios/                    # App de horarios y disponibilidad
│   ├── models.py                # Modelos Horario y Excepcion
│   └── views.py                 # Gestión de horarios
│
├── reportes/                    # App de reportes y dashboards
│   ├── views.py                 # Dashboard admin, reportes
│   └── templates/reportes/      # Templates de reportes
│       └── dashboard_admin_calendario.html  # Dashboard con FullCalendar
│
├── templates/                   # Templates globales
│   ├── base.html                # Template base con navbar
│   └── home.html                # Página de inicio
│
├── static/                      # Archivos estáticos
│   ├── css/                     # Estilos personalizados
│   ├── js/                      # Scripts JavaScript
│   └── images/                  # Imágenes
│
├── media/                       # Archivos subidos (fotos de perfil, etc.)
│
├── manage.py                    # Script de gestión de Django
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

---

## 🔐 Usuarios de Prueba

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Acceso:** Dashboard administrativo completo con calendario

### Doctores
- **Usuario:** `Antonio` | **Contraseña:** `joseS415` | **Especialidad:** Cardiología
- **Usuario:** `josue` | **Contraseña:** `doctor123` | **Especialidad:** Pediatría
- **Usuario:** `carlos` | **Contraseña:** `doctor123` | **Especialidad:** Medicina General

### Pacientes
- **Usuario:** `mike` | **Contraseña:** `joseS415`

---

## 🎯 Validaciones Implementadas

### Validaciones de Citas
- ❌ **No se pueden agendar citas en fechas pasadas**
- ❌ **No se pueden agendar citas fuera del horario laboral** del doctor
- ❌ **No se permite doble reserva** del mismo horario
- ❌ **Validación de días laborables** (si el doctor no trabaja ese día, no se puede agendar)
- ❌ **Validación de excepciones** (vacaciones, bloqueos de agenda)
- ❌ **Hora de fin debe ser mayor a hora de inicio**

### Validaciones de Usuarios
- ✅ **Email único** por usuario
- ✅ **Username único**
- ✅ **DNI único** para pacientes
- ✅ **Contraseñas seguras** (mínimo 6 caracteres)
- ✅ **Validación de formato de email**

### Validaciones de Perfil
- ✅ **Campos requeridos** en registro
- ✅ **Formato de teléfono** válido
- ✅ **Fecha de nacimiento** no puede ser futura

---

## 📈 Funcionalidades Avanzadas

### 🗓️ Calendario Interactivo (FullCalendar)
- **Vista Mes/Semana/Día** navegable
- **Colores por estado:**
  - 🟡 Amarillo = Pendiente
  - 🟢 Verde = Confirmada
  - 🔵 Azul = Completada
  - 🔴 Rojo = Cancelada
- **Modal informativo** al hacer clic en una cita con:
  - Información del paciente
  - Doctor asignado
  - Fecha y hora
  - Estado y motivo
- **Navegación por meses** con botones Anterior/Siguiente
- **Botón "Hoy"** para volver a la fecha actual

### 📊 Reportes con Filtros
- **Filtros múltiples:** Estado, especialidad, doctor, rango de fechas
- **Exportación a Excel** con formato profesional
- **Estadísticas en tiempo real**
- **Gráficos visuales** (próximamente)

### 🔍 Búsqueda Avanzada
- **Búsqueda de doctores** por:
  - Nombre o apellido
  - Especialidad
  - Licencia médica
- **Resultados en tiempo real**
- **Tarjetas visuales** con información completa

### 👤 Sistema de Perfiles
- **Editar perfil completo:**
  - Datos personales
  - Información médica (pacientes)
  - Biografía profesional (doctores)
  - Foto de perfil
- **Cambiar contraseña** con validación
- **Mantener sesión** después de cambiar contraseña

---




## 📝 Guía de Uso

### Para Pacientes:
1. **Registrarse** en el sistema
2. **Buscar doctor** por especialidad
3. **Ver disponibilidad** en el calendario
4. **Agendar cita** seleccionando fecha y hora
5. **Ver mis citas** en el historial
6. **Cancelar** si es necesario (con al menos 24h de anticipación)

### Para Doctores:
1. **Configurar horarios** de atención
2. **Ver agenda** del día/semana
3. **Confirmar citas** pendientes
4. **Atender paciente** registrando diagnóstico y tratamiento
5. **Ver historial** de cada paciente

### Para Administradores:
1. **Ver calendario general** con todas las citas
2. **Generar reportes** con filtros personalizados
3. **Exportar a Excel** para análisis externo
4. **Gestionar** doctores, pacientes y especialidades desde el Admin Django

---

## 🤝 Contribuciones

Este proyecto fue desarrollado con fines **educativos** como proyecto universitario.

---



## 👨‍💻 Autor

**Saucedo Guerrero Jose Dilmer y Grupo 4 Taller de programacion **

Desarrollado como proyecto del curso de Desarrollo de Aplicaciones Web  
Universidad Señor de Sipán - 2025-II

---





