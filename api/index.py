"""
Punto de entrada ASGI para Vercel (api/index.py)

Objetivo para un aprendiz:
- Explicar cómo Vercel invoca una aplicación ASGI de Django.
- Asegurar que Python pueda encontrar el proyecto (`blog`) esté donde esté el repo.
- Exponer una variable `app` que Vercel detecta automáticamente.

Resumen de pasos:
1) Añadimos la raíz del repositorio al PYTHONPATH para poder importar `blog.settings`.
2) Indicamos a Django qué módulo de settings usar.
3) Construimos el objeto ASGI con `get_asgi_application()` y lo exponemos como `app`.
"""

import os
import sys
from pathlib import Path

# 1) Asegura que la raíz del repo está en PYTHONPATH
#    __file__ -> api/index.py
#    parents[1] -> carpeta raíz del repo (contiene manage.py y blog/)
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2) Señala a Django qué settings cargar (el proyecto se llama "blog")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

# Import tardío para que el PYTHONPATH y DJANGO_SETTINGS_MODULE ya estén listos
from django.core.asgi import get_asgi_application  # noqa: E402

# 3) Vercel espera que exportemos una variable llamada `app`
#    Este objeto maneja cada petición ASGI entrante.
app = get_asgi_application()
