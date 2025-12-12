# 🔧 TROUBLESHOOTING - Solución de Problemas Comunes

## ❌ PROBLEMA: "Application failed to respond"

### Causa:
El servidor no puede iniciar correctamente.

### Solución:
1. **Verificar Procfile:**
   ```bash
   cat Procfile
   ```
   Debe contener exactamente: `web: gunicorn config.wsgi --log-file -`

2. **Verificar logs en Railway:**
   - Dashboard → Deployments → Click en el último deploy → Ver logs
   - Buscar errores en rojo

3. **Verificar que gunicorn esté instalado:**
   ```bash
   grep gunicorn requirements.txt
   ```

---

## ❌ PROBLEMA: "No module named 'xxx'"

### Causa:
Falta una dependencia en requirements.txt

### Solución:
```bash
# Agregar la dependencia faltante a requirements.txt
echo "nombre-del-paquete==version" >> requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Agregar dependencia faltante"
git push origin main
```

---

## ❌ PROBLEMA: CSS/JS no cargan (archivos estáticos)

### Causa:
Archivos estáticos no se están sirviendo correctamente.

### Solución:
1. **Verificar WhiteNoise en settings.py:**
   - Debe estar en MIDDLEWARE
   - Debe tener: `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

2. **Ejecutar collectstatic localmente:**
   ```bash
   python manage.py collectstatic --no-input
   ```

3. **Verificar build.sh:**
   Debe contener: `python manage.py collectstatic --no-input`

4. **Verificar en Railway:**
   - Logs del deploy deben mostrar "Collecting static files"

---

## ❌ PROBLEMA: "OperationalError: FATAL: database does not exist"

### Causa:
La base de datos no está conectada o no existe.

### Solución:
1. **Verificar que PostgreSQL esté agregado:**
   - Railway Dashboard → Tu proyecto → Debe haber un servicio PostgreSQL

2. **Verificar DATABASE_URL:**
   - Service Django → Variables → Debe existir `DATABASE_URL`
   - Railway lo crea automáticamente al agregar PostgreSQL

3. **Re-desplegar:**
   - Click en el último deployment
   - Click en "Redeploy"

---

## ❌ PROBLEMA: "DisallowedHost at /"

### Causa:
El dominio no está en ALLOWED_HOSTS.

### Solución:
1. **Verificar variable ALLOWED_HOSTS en Railway:**
   ```
   ALLOWED_HOSTS=*.railway.app
   ```

2. **O agregar dominio específico:**
   ```
   ALLOWED_HOSTS=tu-dominio.railway.app,*.railway.app
   ```

---

## ❌ PROBLEMA: Imágenes de perfil no se guardan (Media files)

### Causa:
Railway no persiste archivos media entre despliegues.

### Solución:
**Para proyecto universitario:**
- Los archivos media se perderán en cada re-deploy
- Esto es normal en Railway sin almacenamiento persistente

**Para producción real:**
- Usar S3 de AWS o Cloudinary para archivos media
- Configurar en settings.py

**Solución temporal:**
```python
# En settings.py para desarrollo
if DEBUG:
    # Archivos locales
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # No usar media files o usar S3
    pass
```

---

## ❌ PROBLEMA: "SECRET_KEY has a dangerous value"

### Causa:
Estás usando la SECRET_KEY por defecto en producción.

### Solución:
```bash
# Generar nueva SECRET_KEY
python generate_secret_key.py

# Copiar la clave generada
# Ir a Railway → Variables → Editar SECRET_KEY
# Pegar la nueva clave
```

---

## ❌ PROBLEMA: Migraciones no se ejecutan

### Causa:
Las migraciones no se corrieron automáticamente.

### Solución:
1. **Verificar build.sh:**
   Debe contener: `python manage.py migrate`

2. **Ejecutar manualmente desde Railway CLI:**
   ```bash
   railway run python manage.py migrate
   ```

3. **Ver logs de migración:**
   - Railway → Deployments → Build logs
   - Buscar: "Running migrations"

---

## ❌ PROBLEMA: "502 Bad Gateway"

### Causa:
El servidor está caído o reiniciándose.

### Solución:
1. **Esperar 2-3 minutos** (Railway puede estar reiniciando)

2. **Verificar logs:**
   - Railway Dashboard → Deployments → Logs
   - Buscar errores

3. **Redeploy manual:**
   - Click en el deployment
   - Click "Redeploy"

---

## ❌ PROBLEMA: No puedo crear superusuario

### Causa:
No hay acceso a terminal o Railway CLI no está configurado.

### Solución:
1. **Instalar Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Conectar:**
   ```bash
   railway login
   railway link
   ```

3. **Crear superusuario:**
   ```bash
   railway run python manage.py createsuperuser
   ```

**ALTERNATIVA:**
- Crear usuario desde código con script de inicialización
- O crear usuario localmente, exportar DB, importar en Railway

---

## ❌ PROBLEMA: El proyecto se "duerme" o se apaga

### Causa:
Railway tiene límite de $5 gratis al mes.

### Solución:
1. **Verificar uso:**
   - Railway Dashboard → Usage
   - Ver cuánto crédito queda

2. **Optimizar:**
   - Railway cobra por tiempo de ejecución
   - ~$0.01 por hora
   - $5 = ~500 horas/mes (suficiente para proyecto universitario)

3. **Si se acaba el crédito:**
   - Agregar tarjeta de crédito (solo cobra lo que uses)
   - O esperar al próximo mes

---

## ❌ PROBLEMA: Cambios no se reflejan después de push

### Causa:
Railway no detectó los cambios o el deploy falló.

### Solución:
1. **Verificar que el push fue exitoso:**
   ```bash
   git log --oneline
   ```

2. **Verificar Railway Dashboard:**
   - Deployments → Debe haber un nuevo deployment
   - Ver si está en "Building" o "Failed"

3. **Forzar re-deploy:**
   - Click en el último deployment
   - Click "Redeploy"

---

## ❌ PROBLEMA: CSRF Token Error

### Causa:
Configuración de seguridad incorrecta.

### Solución:
Agregar en settings.py:
```python
# Para Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://tu-dominio.railway.app',
]
```

Luego:
```bash
git add config/settings.py
git commit -m "Fix CSRF"
git push origin main
```

---

## 📝 LOGS ÚTILES PARA DEBUG

### Ver logs en tiempo real:
```bash
railway logs --follow
```

### Ver últimos 100 logs:
```bash
railway logs --limit 100
```

### Filtrar errores:
```bash
railway logs | grep ERROR
```

---

## 📞 RECURSOS DE AYUDA

1. **Documentación Railway:** https://docs.railway.app/
2. **Discord Railway:** https://discord.gg/railway
3. **Stack Overflow:** Buscar "railway django deploy"

---

## 🎯 CHECKLIST RÁPIDO SI TODO FALLA

- [ ] Procfile existe y es correcto
- [ ] requirements.txt tiene gunicorn, whitenoise, dj-database-url
- [ ] build.sh existe y es ejecutable
- [ ] settings.py tiene configuración de producción
- [ ] PostgreSQL está agregado en Railway
- [ ] Variables de entorno están configuradas
- [ ] Logs no muestran errores críticos
- [ ] Dominio está generado en Railway

---

**Si después de revisar todo esto sigue sin funcionar, copia los logs de Railway y compártelos conmigo.** 🔍
