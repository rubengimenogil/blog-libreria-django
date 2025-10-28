#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Configuración de la app `posts`.
# Django usa esta clase para registrar la aplicación en INSTALLED_APPS.

from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
