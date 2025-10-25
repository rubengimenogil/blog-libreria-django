import os
import sys
from pathlib import Path

# Añadir la raíz del repo al PYTHONPATH para resolver el paquete "blog"
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Configurar Django (proyecto existente: "blog")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

from django.core.asgi import get_asgi_application  # noqa: E402

# Vercel espera un objeto 'app'
app = get_asgi_application()
