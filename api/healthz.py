"""
Minimal ASGI endpoint for Vercel health checks, independent of Django.
This avoids DB connections and framework overhead.
"""

import json


async def app(scope, receive, send):
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
