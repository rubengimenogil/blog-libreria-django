#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tests mínimos de dominio y de vista.
#
# Estrategia:
# - Model: __str__ y ordenación determinista.
# - View index: renderiza, orden correcto y etiqueta <link> al CSS estático.
# - Health: runtime y DB.
#
# Nota: En CI local por defecto usamos SQLite (rápido y determinista).
#       Para probar contra Postgres (p.ej. Neon), activa USE_POSTGRES_FOR_TESTS=1
#       y proporciona DATABASE_URL (véase workflows/ci.yml).

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Post
from django.templatetags.static import static


class PostModelTest(TestCase):
	def test_str(self):
		p = Post.objects.create(title="t", content="c")
		self.assertEqual(str(p), "t")

	def test_default_ordering_desc_by_date(self):
		# Creamos dos posts y ajustamos explícitamente las fechas para evitar
		# empates de timestamp en bases como SQLite (resolución por segundo).
		p1 = Post.objects.create(title="p1", content="c1")
		p2 = Post.objects.create(title="p2", content="c2")
		p1.published_date = timezone.now() - timedelta(minutes=1)
		p1.save(update_fields=["published_date"])
		p2.published_date = timezone.now()
		p2.save(update_fields=["published_date"])
		self.assertEqual(list(Post.objects.all()), [p2, p1])


class PostListViewTest(TestCase):
	def test_index_renders_and_orders(self):
		p1 = Post.objects.create(title="A", content="c1")
		p2 = Post.objects.create(title="B", content="c2")
		url = reverse("post_list")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		# Titles should appear with p2 before p1
		content = resp.content.decode()
		self.assertTrue(content.index("B") < content.index("A"))

	def test_index_links_correct_static_css(self):
		# Render home and ensure the CSS href points to our static path
		resp = self.client.get(reverse("post_list"))
		self.assertEqual(resp.status_code, 200)
		expected_css = static("post/style.css")
		self.assertIn(expected_css, resp.content.decode())


class HealthEndpointsTest(TestCase):
	def test_healthz_ok(self):
		resp = self.client.get(reverse("healthz"))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json().get("ok"), True)

	def test_db_healthz_ok(self):
		resp = self.client.get(reverse("db_healthz"))
		self.assertEqual(resp.status_code, 200)
		body = resp.json()
		self.assertTrue(body.get("ok"))
		self.assertTrue(body.get("db"))
		self.assertEqual(body.get("result"), 1)
