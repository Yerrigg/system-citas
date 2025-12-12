# 🚀 GUÍA DE DESPLIEGUE EN RAILWAY - System Citas

## 📋 ARCHIVOS PREPARADOS

Los siguientes archivos ya están listos en tu proyecto:

✅ `runtime.txt` - Especifica la versión de Python
✅ `Procfile` - Le dice a Railway cómo ejecutar la app
✅ `requirements.txt` - Actualizado con dependencias para producción
✅ `build.sh` - Script de construcción automático
✅ `config/settings.py` - Configurado para desarrollo y producción
✅ `.env.example` - Ejemplo de variables de entorno

---

## 🎯 PASOS PARA DESPLEGAR EN RAILWAY

### **PASO 1: Subir cambios a GitHub**

```bash
# Desde la carpeta Y:\Downloads\system-citas

# 1. Agregar todos los archivos nuevos
git add .

# 2. Hacer commit
git commit -m "Preparar proyecto para despliegue en Railway"

# 3. Subir a GitHub
git push origin main
```

**IMPORTANTE:** Si tu rama principal se llama `master` en lugar de `main`, usa:
```bash
git push origin master
```

---

### **PASO 2: Crear cuenta en Railway**

1. Ve a: **https://railway.app/**
2. Click en **"Start a New Project"** o **"Login"**
3. Inicia sesión con tu cuenta de GitHub
4. Autoriza a Railway para acceder a tus repositorios

---

### **PASO 3: Crear nuevo proyecto**

1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca tu repositorio: `system-citas`
4. Click en el repositorio para seleccionarlo

---

### **PASO 4: Agregar PostgreSQL**

1. En tu proyecto de Railway, click en **"+ New"**
2. Selecciona **"Database"**
3. Selecciona **"Add PostgreSQL"**
4. Railway creará automáticamente la base de datos

---

### **PASO 5: Configurar variables de entorno**

1. Click en tu servicio de Django (el que dice "system-citas")
2. Ve a la pestaña **"Variables"**
3. Click en **"+ Add Variable"** y agrega las siguientes:

```env
SECRET_KEY=tu-secret-key-super-secreta-cambiala-ahora-123456789
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**IMPORTANTE:** 
- Cambia `SECRET_KEY` por una clave única y segura
- Puedes generar una en: https://djecrety.ir/

Railway automáticamente creará y conectará la variable `DATABASE_URL` desde PostgreSQL.

---

### **PASO 6: Verificar el despliegue**

1. Railway comenzará a construir tu proyecto automáticamente
2. Puedes ver los logs en la pestaña **"Deployments"**
3. Espera a que termine (puede tardar 5-10 minutos)
4. Verás un mensaje: **"Success - Build completed"**

---

### **PASO 7: Obtener la URL de tu aplicación**

1. En la pestaña **"Settings"** de tu servicio
2. Busca la sección **"Domains"**
3. Click en **"Generate Domain"**
4. Railway te dará una URL como: `https://system-citas-production-XXXX.up.railway.app`

---

### **PASO 8: Crear superusuario (Administrador)**

1. Ve a la pestaña **"Settings"** de tu servicio
2. Busca **"Service Settings"**
3. Abre una **terminal** (o usa Railway CLI)
4. Ejecuta:

```bash
python manage.py createsuperuser
```

Ingresa:
- Username: `admin`
- Email: `admin@systemcitas.com`
- Password: (la que prefieras)

**ALTERNATIVA:** Si no hay terminal en el dashboard, instala Railway CLI:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Crear superusuario
railway run python manage.py createsuperuser
```

---

### **PASO 9: Cargar datos iniciales (Opcional)**

Si quieres crear especialidades y doctores de prueba:

1. Accede al admin de Django: `https://tu-url.railway.app/admin/`
2. Login con el superusuario
3. Crea especialidades (Cardiología, Pediatría, etc.)
4. Crea usuarios tipo "Doctor" y sus perfiles

---

## ✅ VERIFICACIÓN FINAL

Accede a tu aplicación:
- **URL principal:** `https://tu-url.railway.app/`
- **Admin Django:** `https://tu-url.railway.app/admin/`

Prueba:
- ✅ Registro de usuario
- ✅ Login
- ✅ Dashboard
- ✅ Agendar citas

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "Application failed to respond"
- Verifica que `Procfile` esté correcto
- Revisa los logs en Railway
- Asegúrate de que `gunicorn` esté en `requirements.txt`

### Error: "No module named 'xxx'"
- Falta una dependencia en `requirements.txt`
- Agrégala y haz `git push`

### Error de base de datos
- Verifica que PostgreSQL esté conectado
- Railway debe crear automáticamente `DATABASE_URL`
- Revisa los logs de migración

### Archivos estáticos no cargan
- `WhiteNoise` se encarga de esto automáticamente
- Verifica que `collectstatic` se ejecutó en el build

---

## 💰 LÍMITES DEL PLAN GRATUITO

Railway te da **$5 USD de crédito gratis al mes**, que equivale a:
- **~500 horas de ejecución** (más que suficiente)
- Base de datos PostgreSQL incluida
- Sin tarjeta de crédito requerida

---

## 🔄 ACTUALIZAR LA APLICACIÓN

Para hacer cambios y actualizar:

```bash
# 1. Hacer cambios en tu código
# 2. Commit
git add .
git commit -m "Descripción de cambios"

# 3. Push a GitHub
git push origin main

# Railway detectará los cambios y desplegará automáticamente
```

---

## 📞 SOPORTE

Si tienes problemas:
1. Revisa los logs en Railway Dashboard
2. Consulta la documentación: https://docs.railway.app/
3. Comparte los errores conmigo para ayudarte

---

**¡LISTO! Tu sistema de citas médicas estará en producción en minutos.** 🎉
