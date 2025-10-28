"""
Configuración WSGI para Django.

Para un aprendiz:
- WSGI es el protocolo clásico (sincrónico) para apps Python.
- `application` es el callable que servidores como Gunicorn/uwsgi invocan.
- Aunque en Vercel usamos ASGI, `wsgi.py` sigue siendo útil en local y otros entornos.
"""

import os

from django.core.wsgi import get_wsgi_application

# Señala al proceso qué settings de Django debe cargar.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Construye el objeto WSGI listo para recibir peticiones.
application = get_wsgi_application()
