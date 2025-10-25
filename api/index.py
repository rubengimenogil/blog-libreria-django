# contenedor/api/index.py
import os
import sys
from pathlib import Path

# Asegurar que el root del proyecto esté en sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Configuración Django (el proyecto se llama "blog")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

from django.core.asgi import get_asgi_application  # noqa: E402

# Vercel espera una variable "app"
app = get_asgi_application()
