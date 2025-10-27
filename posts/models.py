from django.db import models


class Post(models.Model):
    """Entrada de blog sencilla.

    Campos:
    - title: título de la entrada (200 chars)
    - content: contenido libre en texto
    - published_date: fecha de publicación, se fija automáticamente al crear
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]  # orden por defecto: más recientes primero

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title
