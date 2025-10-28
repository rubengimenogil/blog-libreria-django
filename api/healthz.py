#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ASGI mínimo para `/healthz` en Vercel, independiente de Django.

Motivación:
- Evitar arrancar Django/ORM solo para un ping de salud.
- No abre conexiones a la base de datos.
- Responde JSON muy pequeño y no cacheable.

En `vercel.json` está mapeado con:
  { "src": "/healthz/?", "dest": "api/healthz.py" }
"""

import json


async def app(scope, receive, send):
    # Compatibilidad con HTTP/HTTPS en entornos ASGI
    assert scope["type"] in {"http", "https"}
    body = json.dumps({"ok": True}).encode("utf-8")
    headers = [
        (b"content-type", b"application/json; charset=utf-8"),
        (b"cache-control", b"no-store"),
    ]
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": headers,
    })
    await send({
        "type": "http.response.body",
        "body": body,
    })
