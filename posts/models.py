#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Modelo de dominio principal: Post.
#
# Decisiones de diseño:
# - `published_date` con auto_now_add fija la fecha al crear.
# - Meta.ordering define orden estable de más reciente a más antiguo;
#   en caso de empates exactos de timestamp, usa `-id` para desempatar.

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
