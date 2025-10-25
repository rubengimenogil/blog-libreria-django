# contenedor/api/index.py
import os, sys
from pathlib import Path

# Añade la carpeta del proyecto (donde está manage.py) al sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Apunta al settings de tu proyecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

# Expone la aplicación WSGI que Vercel necesita
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
