#!/usr/bin/env python
"""Utility de línea de comandos de Django.

Casos de uso comunes:
- `python manage.py runserver` → arranca servidor de desarrollo (WSGI).
- `python manage.py migrate` → aplica migraciones.
- `python manage.py createsuperuser` → crea usuario admin.
- `python manage.py collectstatic` → compila estáticos a STATIC_ROOT.

Este archivo fija DJANGO_SETTINGS_MODULE y delega en Django para ejecutar
los comandos indicados. En este proyecto, el despliegue en Vercel usa ASGI
desde `api/index.py`, pero mantener WSGI/CLI es clave para el flujo dev local.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
