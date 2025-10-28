#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Rutas de la app `posts`.
# - Home ('') lista entradas.
# - `/healthz/` comprueba que el runtime Django responde.
# - `/db-healthz/` prueba SELECT 1 contra la base de datos.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('healthz/', views.healthz, name='healthz'),
    path('db-healthz/', views.db_healthz, name='db_healthz'),
    path('static-healthz/', views.static_healthz, name='static_healthz'),
    path('template-debug/', views.template_debug, name='template_debug'),
]
