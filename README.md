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
  - vercel.json con:
    - installCommand: pip install -r contenedor/requirements.txt
    - buildCommand: python manage.py collectstatic --noinput
    - rutas: /static -> staticfiles, resto -> contenedor/api/index.py
  - Entry ASGI: contenedor/api/index.py (DJANGO_SETTINGS_MODULE=blog.settings)

Pasos

1) Importar repo en Vercel.
2) Variables de entorno en Vercel (Project Settings -> Environment Variables):
   - SECRET_KEY
   - DEBUG=0
   - DATABASE_URL=postgres://... (por ejemplo, Neon con sslmode=require)
   - ALLOWED_HOSTS=blog-libreria-django.vercel.app,localhost,127.0.0.1
3) Deploy. Tras el primer deploy, ejecutar migraciones:
   - Opcionalmente con Vercel CLI: vercel env pull && vercel build
   - O bien correr migrate localmente apuntando a la misma DATABASE_URL.
4) Acceder a https://<tu-dominio>.vercel.app/

Notas

- Asegúrate de que STATIC_ROOT en settings apunta a "staticfiles" para que collectstatic funcione.
- La app de contenido es "posts"; define rutas y vistas propias (no incluidas aquí).
