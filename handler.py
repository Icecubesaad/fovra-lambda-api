"""Serverless HTTP API — FastAPI + Mangum adapter for AWS Lambda.

One deployable function (`app`) fronted by Lambda Function URLs /
HTTP API. Pure request/response workloads: no long-lived connections,
no background loops — the canonical fit for a serverless compute tier.
"""
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app_fastapi = FastAPI(title="fovra-lambda-api")

# Tiny in-memory store: a real deployment would use DynamoDB or RDS.
_LINKS = {
    "fovra": "https://github.com/Icecubesaad",
}


@app_fastapi.get("/health")
def health():
    return {"ok": True, "service": "lambda-api"}


@app_fastapi.get("/links")
def list_links():
    return {"links": _LINKS}


class LinkCreate(BaseModel):
    slug: str = ""
    target: str = ""


@app_fastapi.post("/links", status_code=201)
def create_link(body: LinkCreate):
    slug = body.slug.strip()
    target = body.target.strip()
    if not slug or not target:
        raise HTTPException(status_code=400, detail="slug and target are required")
    _LINKS[slug] = target
    return {"slug": slug, "target": target}


@app_fastapi.get("/links/{slug}")
def resolve_link(slug: str):
    target = _LINKS.get(slug)
    if not target:
        raise HTTPException(status_code=404, detail="not found")
    return {"slug": slug, "target": target}


# Lambda entrypoint: the Runtime API event loop bridges through Mangum.
app = Mangum(app_fastapi, lifespan="off")


@app_fastapi.get("/version")
def version():
    return {"release": "B"}
