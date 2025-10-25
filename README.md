# Blog Librería (Django) — proyecto "blog", app "posts"

Guía rápida

- Entorno
  - Python 3.11+
  - Variables en `.env`: SECRET_KEY, DEBUG, DATABASE_URL, (opcional) ALLOWED_HOSTS

- Instalar dependencias
  - pip install -r contenedor/requirements.txt

- Migraciones y superusuario
  - python manage.py migrate
  - python manage.py createsuperuser

- Ejecutar en local
  - python manage.py runserver
  - http://127.0.0.1:8000/  (rutas definidas en la app posts)
  - http://127.0.0.1:8000/admin/

Despliegue en Vercel

- Root Directory del proyecto en Vercel: `contenedor`
- Configuración:
  - `contenedor/vercel.json` con:
    - `functions: { "api/*.py": { runtime: "python3.11" } }`
    - `rewrites` hacia `/api/index.py`
  - Entry ASGI: `contenedor/api/index.py` (DJANGO_SETTINGS_MODULE=blog.settings)
  - Dependencias: `contenedor/requirements.txt`
- Importante: mantener solo una API
  - Usa `contenedor/api/index.py`
  - Elimina la carpeta `api/` del raíz si existe (evita duplicados)

Comprobaciones

- `contenedor/api/index.py` expone `app = get_asgi_application()`
- `contenedor/requirements.txt` contiene Django y deps necesarias
- Variables en Vercel:
  - SECRET_KEY, DEBUG=0, DATABASE_URL, ALLOWED_HOSTS
- Tras el deploy:
  - No se ejecuta `collectstatic` automáticamente. Si necesitas estáticos del admin, añade WhiteNoise o un CDN.

Notas
- El `vercel.json` de la raíz queda como fallback (no se usa cuando el Root Directory es `contenedor`).
