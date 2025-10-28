"""
Configuración ASGI estándar para Django.

Para un aprendiz:
- ASGI es el protocolo moderno para apps Python asíncronas (sustituto/compañero de WSGI).
- Django expone un callable llamado `application` que el servidor ASGI invoca por request.
- En Vercel usamos `api/index.py`, pero tener este archivo correcto ayuda en otros despliegues.
"""

import os
from django.core.asgi import get_asgi_application

# Indica a Django qué settings cargar por defecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

# Objeto ASGI que procesa las peticiones entrantes
application = get_asgi_application()

