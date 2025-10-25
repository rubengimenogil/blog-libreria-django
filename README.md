# Blog Librería (Django) — proyecto "blog", app "posts"

Guía rápida

- Entorno
  - Python 3.11+
  - Variables en `.env`: SECRET_KEY, DEBUG, DATABASE_URL, (opcional) ALLOWED_HOSTS

- Instalar dependencias
  - pip install -r requirements.txt

- Migraciones y superusuario
  - python manage.py migrate
  - python manage.py createsuperuser

- Ejecutar en local
  - python manage.py runserver
  - http://127.0.0.1:8000/  (rutas definidas en la app posts)
  - http://127.0.0.1:8000/admin/

Despliegue en Vercel

- Configuración (vercel.json en la raíz):
  - builds: [{ src: "api/index.py", use: "@vercel/python" }]
  - installCommand: pip install -r requirements.txt
  - buildCommand: python manage.py collectstatic --noinput
  - rutas: /static -> staticfiles y resto -> api/index.py
- Entry ASGI: api/index.py (DJANGO_SETTINGS_MODULE=blog.settings)
- Requisitos:
  - requirements.txt en la raíz con dependencias de Django
  - STATIC_ROOT en settings -> BASE_DIR / "staticfiles"
  - Variables en Vercel: SECRET_KEY, DEBUG=0, DATABASE_URL, ALLOWED_HOSTS

Notas
- El aviso “Due to builds existing... Settings will not apply” es normal cuando hay `builds` en vercel.json; se usarán los comandos definidos en el archivo.
- Mantén un único vercel.json (el de la raíz) y elimina otros para evitar conflictos.
- Asegúrate de que `api/index.py` expone `app = get_asgi_application()` y `STATIC_ROOT` apunta a `staticfiles`.
