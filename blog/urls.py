#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enrutado global del proyecto Django.

Decisiones:
- La raíz ('') se delega a la app `posts` para que sirva la home del blog.
- La administración nativa de Django queda en `/admin/`.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]
