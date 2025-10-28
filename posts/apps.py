from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Metadatos de la app `posts`.

    Para un aprendiz:
    - Django detecta apps por su AppConfig.
    - default_auto_field define el tipo de clave primaria por defecto.
    - name indica la ruta del paquete de la app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
