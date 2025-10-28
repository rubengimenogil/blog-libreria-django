"""
ASGI mínimo para /healthz (sin tocar Django ni la base de datos).

Pasos para un aprendiz:
- ASGI define una función/objeto callable que recibe tres cosas: (scope, receive, send).
- scope describe la conexión (tipo http, headers de entrada, ruta, etc.).
- receive permite leer mensajes entrantes (no necesitamos para una respuesta simple).
- send nos deja enviar mensajes de salida (cabecera y cuerpo de la respuesta).

Con esto devolvemos un JSON muy pequeño, útil para que Vercel o un monitor
verifique que el runtime está vivo sin depender de la BD.
"""

import json


async def app(scope, receive, send):
    # 1) Validamos que la conexión es HTTP/HTTPS (ASGI soporta websockets, etc.)
    assert scope["type"] in {"http", "https"}

    # 2) Preparamos el cuerpo de respuesta (bytes) y cabeceras HTTP
    body = json.dumps({"ok": True}).encode("utf-8")
    headers = [
        (b"content-type", b"application/json; charset=utf-8"),
        (b"cache-control", b"no-store"),  # no caches para health checks
    ]

    # 3) Enviamos el inicio de la respuesta (status y headers)
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": headers,
    })

    # 4) Enviamos el cuerpo y cerramos
    await send({
        "type": "http.response.body",
        "body": body,
    })
