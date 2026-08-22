"""Serverless HTTP API — Flask + Mangum adapter for AWS Lambda.

One deployable function (`app`) fronted by Lambda Function URLs /
HTTP API. Pure request/response workloads: no long-lived connections,
no background loops — the canonical fit for a serverless compute tier.
"""
from mangum import Mangum
from flask import Flask, jsonify

flask_app = Flask(__name__)

# Tiny in-memory store: a real deployment would use DynamoDB or RDS.
_LINKS = {
    "fovra": "https://github.com/Icecubesaad",
}


@flask_app.get("/health")
def health():
    return jsonify(ok=True, service="lambda-api")


@flask_app.get("/links")
def list_links():
    return jsonify(links=_LINKS)


@flask_app.post("/links")
def create_link():
    from flask import request

    slug = (request.json or {}).get("slug", "").strip()
    target = (request.json or {}).get("target", "").strip()
    if not slug or not target:
        return jsonify(error="slug and target are required"), 400
    _LINKS[slug] = target
    return jsonify(slug=slug, target=target), 201


@flask_app.get("/links/<slug>")
def resolve_link(slug: str):
    target = _LINKS.get(slug)
    if not target:
        return jsonify(error="not found"), 404
    return jsonify(slug=slug, target=target)


# Lambda entrypoint: the Runtime API event loop bridges through Mangum.
app = Mangum(flask_app, lifespan="off")
