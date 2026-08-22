# fovra-lambda-api

A small URL-shortener API built as a **serverless HTTP function**:
Flask wrapped in [Mangum](https://mangum.io/) so the same app runs on
AWS Lambda behind an HTTP API / Function URL.

## Endpoints

- `GET /health` — liveness
- `GET /links` — list slugs
- `POST /links` `{slug, target}` — create
- `GET /links/<slug>` — resolve

## Why this shape

Request/response only, sub-second cold starts, zero idle cost — the
reference shape for the `lambda_http` compute tier.
