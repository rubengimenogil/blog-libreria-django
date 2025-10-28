#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Punto de entrada ASGI para Vercel.
#
# Qué hace:
# - Asegura que la raíz del repositorio está en PYTHONPATH para que Python
#   pueda importar el proyecto Django ("blog").
# - Fija la variable de entorno DJANGO_SETTINGS_MODULE.
# - Expone la aplicación ASGI como `app` (Vercel la espera con ese nombre).
#
# Cuándo se usa:
# - En producción, nuestras rutas de vercel.json envían todas las
#   peticiones (menos /static y /healthz) a este archivo.
# - Esto arranca el stack ASGI de Django y, con WhiteNoise, servirá
#   también archivos estáticos si fuese necesario (aunque en Vercel
#   usamos una ruta directa a staticfiles/ para eficiencia).

import os
import sys
from pathlib import Path

# Asegura que la raíz del repo está en PYTHONPATH
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Proyecto Django (ya creado): "blog"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

from django.core.asgi import get_asgi_application  # noqa: E402

# Vercel espera 'app'
app = get_asgi_application()
