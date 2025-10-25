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

- Este repositorio incluye:
  - vercel.json (version: 2) con:
    - builds: [{ src: "contenedor/api/index.py", use: "@vercel/python" }]
    - installCommand: pip install -r contenedor/requirements.txt
    - buildCommand: python manage.py collectstatic --noinput
    - rutas: /static -> staticfiles, resto -> contenedor/api/index.py
  - Entry ASGI requerido: contenedor/api/index.py (DJANGO_SETTINGS_MODULE=blog.settings)

Comprobaciones

- Verifica que el archivo contenedor/api/index.py exista y exponga `app = get_asgi_application()`.
- En Vercel (Project Settings -> Build & Development Settings):
  - Framework: Other
  - Output Directory: vacío
  - No overrides de Install/Build Command (si existen, pon los mismos que en vercel.json).
- Re-deploy y revisa el log:
  - Debe aparecer el uso de @vercel/python y la instalación desde contenedor/requirements.txt.

Notas

- Asegúrate de que STATIC_ROOT en settings apunta a "staticfiles" para que collectstatic funcione.
- La app de contenido es "posts"; define rutas y vistas propias (no incluidas aquí).
