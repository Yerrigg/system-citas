from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario
from pacientes.models import Paciente

def home(request):
    """Página de inicio con redirección según rol"""
    
    # Si el usuario está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        
        # Redirigir doctores a su dashboard
        if request.user.rol == 'doctor':
            return redirect('dashboard_doctor')
        
        # Redirigir administradores a su dashboard
        elif request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard_admin')
        
        # Pacientes ven el home normal (con opciones de agendar citas)
    
    # Usuarios no autenticados ven la página de inicio
    return render(request, 'home.html')

def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')

def registro_view(request):
    """Vista de registro"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Datos del usuario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        
        # Datos del paciente
        dni = request.POST.get('dni')
        
        # Validaciones
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuarios/registro.html')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuarios/registro.html')
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'usuarios/registro.html')
        
        if Paciente.objects.filter(dni=dni).exists():
            messages.error(request, 'El DNI ya está registrado.')
            return render(request, 'usuarios/registro.html')
        
        # Crear usuario
        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            telefono=telefono,
            rol='paciente'
        )
        
        # Crear paciente
        Paciente.objects.create(
            usuario=user,
            dni=dni
        )
        
        messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
        return redirect('login')
    
    return render(request, 'usuarios/registro.html')

def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')

@login_required
def perfil_usuario(request):
    """Ver perfil del usuario"""
    usuario = request.user
    
    # Obtener perfil específico según rol
    perfil_especifico = None
    if hasattr(usuario, 'paciente'):
        perfil_especifico = usuario.paciente
    elif hasattr(usuario, 'doctor'):
        perfil_especifico = usuario.doctor
    
    context = {
        'usuario': usuario,
        'perfil_especifico': perfil_especifico,
    }
    
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    """Editar perfil del usuario"""
    usuario = request.user
    
    if request.method == 'POST':
        # Datos básicos del usuario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        
        # Validar email único (excepto el propio)
        if Usuario.objects.filter(email=email).exclude(id=usuario.id).exists():
            messages.error(request, 'Este email ya está registrado por otro usuario.')
            return redirect('editar_perfil')
        
        # Actualizar usuario
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email
        usuario.telefono = telefono
        
        if fecha_nacimiento:
            from datetime import datetime
            try:
                usuario.fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except:
                pass
        
        # Manejar foto de perfil
        if 'foto' in request.FILES:
            usuario.foto = request.FILES['foto']
        
        usuario.save()
        
        # Actualizar datos específicos según rol
        if usuario.rol == 'paciente' and hasattr(usuario, 'paciente'):
            paciente = usuario.paciente
            paciente.direccion = request.POST.get('direccion', '')
            paciente.grupo_sanguineo = request.POST.get('grupo_sanguineo', '')
            paciente.alergias = request.POST.get('alergias', '')
            paciente.contacto_emergencia = request.POST.get('contacto_emergencia', '')
            paciente.telefono_emergencia = request.POST.get('telefono_emergencia', '')
            paciente.save()
        
        elif usuario.rol == 'doctor' and hasattr(usuario, 'doctor'):
            doctor = usuario.doctor
            doctor.biografia = request.POST.get('biografia', '')
            doctor.save()
        
        messages.success(request, '¡Perfil actualizado correctamente!')
        return redirect('perfil_usuario')
    
    # Obtener perfil específico
    perfil_especifico = None
    if hasattr(usuario, 'paciente'):
        perfil_especifico = usuario.paciente
    elif hasattr(usuario, 'doctor'):
        perfil_especifico = usuario.doctor
    
    context = {
        'usuario': usuario,
        'perfil_especifico': perfil_especifico,
    }
    
    return render(request, 'usuarios/editar_perfil.html', context)

@login_required
def cambiar_password(request):
    """Cambiar contraseña del usuario"""
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('cambiar_password')
        
        # Validar que las nuevas contraseñas coincidan
        if password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return redirect('cambiar_password')
        
        # Validar longitud mínima
        if len(password_nueva) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('cambiar_password')
        
        # Cambiar contraseña
        request.user.set_password(password_nueva)
        request.user.save()
        
        # Mantener la sesión activa después de cambiar contraseña
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, '¡Contraseña cambiada exitosamente!')
        return redirect('perfil_usuario')
    
    return render(request, 'usuarios/cambiar_password.html')