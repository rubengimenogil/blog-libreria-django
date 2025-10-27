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
        # Orden por defecto: más recientes primero; si hay empates de timestamp,
        # desempatamos por ID descendente para una lista estable.
        ordering = ["-published_date", "-id"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title
