# contenedor/api/index.py
import os
import sys
from pathlib import Path

# Asegura que la raíz del repo está en PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Proyecto Django (ya creado): "blog"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

from django.core.asgi import get_asgi_application  # noqa: E402

# Vercel espera 'app'
app = get_asgi_application()
