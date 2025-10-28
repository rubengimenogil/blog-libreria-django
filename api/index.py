# contenedor/api/index.py
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
