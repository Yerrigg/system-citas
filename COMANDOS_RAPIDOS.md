# ⚡ COMANDOS RÁPIDOS PARA COPIAR Y PEGAR

## 🔹 PASO 1: Generar SECRET_KEY
```bash
cd Y:\Downloads\system-citas
python generate_secret_key.py
```

---

## 🔹 PASO 2: Subir a GitHub
```bash
git add .
git commit -m "Preparar proyecto para Railway - Despliegue producción"
git push origin main
```

*(Si tu rama principal es master, usa `git push origin master`)*

---

## 🔹 PASO 3: Instalar Railway CLI (Opcional, solo si necesitas terminal)
```bash
npm install -g @railway/cli
```

---

## 🔹 PASO 4: Conectar con Railway CLI (Opcional)
```bash
railway login
railway link
```

---

## 🔹 PASO 5: Crear superusuario desde Railway CLI
```bash
railway run python manage.py createsuperuser
```

---

## 🔹 COMANDOS ÚTILES DESPUÉS DEL DESPLIEGUE

### Ver logs en Railway:
```bash
railway logs
```

### Ejecutar migraciones manualmente:
```bash
railway run python manage.py migrate
```

### Recolectar archivos estáticos:
```bash
railway run python manage.py collectstatic --no-input
```

### Abrir shell de Django:
```bash
railway run python manage.py shell
```

---

## 🔹 VARIABLES DE ENTORNO PARA RAILWAY (Copiar valores)

```
SECRET_KEY=(pega aquí la clave que generaste)
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

---

## 🔹 PROBAR LOCALMENTE ANTES DE DESPLEGAR

### Instalar dependencias actualizadas:
```bash
pip install -r requirements.txt
```

### Recolectar archivos estáticos:
```bash
python manage.py collectstatic --no-input
```

### Ejecutar servidor con gunicorn (como en producción):
```bash
gunicorn config.wsgi --bind 0.0.0.0:8000
```

---

## 🔹 COMANDOS GIT ÚTILES

### Ver estado:
```bash
git status
```

### Ver cambios:
```bash
git diff
```

### Ver historial:
```bash
git log --oneline
```

### Deshacer último commit (SIN perder cambios):
```bash
git reset --soft HEAD~1
```

---

## 🔹 ACTUALIZAR PROYECTO DESPUÉS DE CAMBIOS

```bash
git add .
git commit -m "Descripción de tus cambios"
git push origin main
```

Railway desplegará automáticamente los cambios.

---

## 🔹 ENLACES IMPORTANTES

- **Railway Dashboard:** https://railway.app/dashboard
- **Documentación Railway:** https://docs.railway.app/
- **Generar SECRET_KEY online:** https://djecrety.ir/
- **Tu proyecto:** (guarda aquí la URL de tu proyecto en Railway)

---

## 🔹 SOLUCIÓN RÁPIDA DE PROBLEMAS

### Error: "Application failed to respond"
```bash
# Verificar Procfile
cat Procfile
# Debe mostrar: web: gunicorn config.wsgi --log-file -
```

### Error: "No module named 'gunicorn'"
```bash
# Verificar requirements.txt
grep gunicorn requirements.txt
# Si no está, agrégalo y push de nuevo
```

### Error de base de datos
```bash
# Verificar que DATABASE_URL existe en Railway
railway variables
```

---

**¡Listo! Con estos comandos tienes todo lo necesario para desplegar.** 🚀
