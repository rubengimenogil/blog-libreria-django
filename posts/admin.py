from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	"""Configuración del panel de administración para el modelo Post.

	Para un aprendiz:
	- list_display: columnas que verás en la tabla de listado.
	- search_fields: campos por los que puedes buscar.
	- ordering: orden por defecto (aquí, más nuevos primero).
	"""
	list_display = ("title", "published_date")
	search_fields = ("title", "content")
	ordering = ("-published_date",)
