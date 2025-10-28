"""
WSGI del proyecto "blog" (usado por `runserver` y servidores WSGI clásicos).

En este proyecto desplegamos en Vercel con ASGI (véase `api/index.py`).
Sin embargo, mantener WSGI configurado permite:
- Ejecutar `manage.py runserver` en local sin cambios.
- Compatibilidad con herramientas/hostings que aún esperen WSGI.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

application = get_wsgi_application()
