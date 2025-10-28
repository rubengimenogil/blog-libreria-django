#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ASGI para `/static-healthz` sin arrancar Django.

Qué hace:
- Lee el manifest generado por `collectstatic` en `staticfiles/staticfiles.json`.
- Busca la entrada para `post/style.css` y devuelve la URL hasheada (`/static/...`).
- Si el manifest no existe o no contiene la clave, responde con ok=false y el motivo.

Ventaja:
- Evita depender del enrutado de Django para esta comprobación y nos da
  un diagnóstico claro en Vercel cuando la home devuelve 500 por
  problemas de estáticos/manifest.
"""

import json
from pathlib import Path


async def app(scope, receive, send):
    assert scope["type"] in {"http", "https"}

    base_dir = Path(__file__).resolve().parents[1]
    manifest_path = base_dir / "staticfiles" / "staticfiles.json"
    result = {"ok": False}
    status = 200

    try:
        if not manifest_path.exists():
            result.update({
                "ok": False,
                "error": "manifest_not_found",
                "hint": "No se encuentra staticfiles/staticfiles.json. ¿Se ejecutó collectstatic?",
            })
        else:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            paths = (data or {}).get("paths", {})
            key = "post/style.css"
            hashed = paths.get(key)
            if hashed:
                result.update({
                    "ok": True,
                    "url": f"/static/{hashed}",
                    "source": key,
                })
            else:
                result.update({
                    "ok": False,
                    "error": "missing_manifest_entry",
                    "missing_key": key,
                    "hint": "El manifest existe pero no contiene la entrada del CSS. Revisa collectstatic.",
                })
    except Exception as exc:
        status = 500
        result = {"ok": False, "error": str(exc)}

    body = json.dumps(result).encode("utf-8")
    headers = [
        (b"content-type", b"application/json; charset=utf-8"),
        (b"cache-control", b"no-store"),
    ]
    await send({
        "type": "http.response.start",
        "status": status,
        "headers": headers,
    })
    await send({
        "type": "http.response.body",
        "body": body,
    })
