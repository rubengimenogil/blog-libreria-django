import os
from django.core.wsgi import get_wsgi_application

# Asegúrate de que 'blog.settings' sea el nombre correcto de tu módulo de configuración.
# Si tu settings.py está en una carpeta diferente, ajústalo (por ejemplo "mysite.settings").
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

# Vercel busca esta variable pública llamada 'app'
app = get_wsgi_application()
