# ✅ CHECKLIST RÁPIDO - DESPLIEGUE RAILWAY

## ANTES DE SUBIR A GITHUB

- [ ] Archivos creados correctamente:
  - [ ] `runtime.txt`
  - [ ] `Procfile`
  - [ ] `requirements.txt` actualizado
  - [ ] `build.sh`
  - [ ] `config/settings.py` actualizado
  
- [ ] Generar SECRET_KEY segura:
  ```bash
  python generate_secret_key.py
  ```

- [ ] Subir a GitHub:
  ```bash
  git add .
  git commit -m "Preparar para Railway"
  git push origin main
  ```

---

## EN RAILWAY

### 1. Crear proyecto
- [ ] Ir a https://railway.app/
- [ ] Login con GitHub
- [ ] New Project → Deploy from GitHub repo
- [ ] Seleccionar `system-citas`

### 2. Agregar PostgreSQL
- [ ] Click "+ New" → Database → PostgreSQL
- [ ] Esperar a que se cree

### 3. Configurar variables
- [ ] Click en servicio Django → Variables
- [ ] Agregar:
  ```
  SECRET_KEY=(la generada con generate_secret_key.py)
  DEBUG=False
  ALLOWED_HOSTS=*.railway.app
  ```

### 4. Generar dominio
- [ ] Settings → Domains → Generate Domain
- [ ] Copiar URL

### 5. Crear superusuario
- [ ] Settings → Abrir terminal
- [ ] `python manage.py createsuperuser`

---

## VERIFICACIÓN

- [ ] Abrir la URL de Railway
- [ ] Probar login
- [ ] Probar registro de paciente
- [ ] Acceder al admin

---

## 🎉 ¡LISTO! Tu sistema está en producción
