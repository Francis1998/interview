#!/usr/bin/env python3
"""Serve the Interview Handbook web preview."""

from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"

TOPIC_FILES = {
    "python": "python.md",
    "golang": "golang.md",
    "mysql": "mysql.md",
    "linux": "linux.md",
    "networking": "networking.md",
    "operating-systems": "operating-systems.md",
    "redis": "redis.md",
    "algorithms": "algorithms.md",
    "system-design": "system-design.md",
}


def create_app() -> FastAPI:
    """Build FastAPI app for handbook preview."""
    app = FastAPI(title="Interview Handbook", version="1.0.0")
    app.mount("/static", StaticFiles(directory=str(DEMO / "static")), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> FileResponse:
        return FileResponse(DEMO / "index.html")

    @app.get("/health")
    async def health() -> dict[str, str | int]:
        return {"status": "ok", "topics": len(TOPIC_FILES)}

    @app.get("/api/topics")
    async def list_topics() -> list[dict[str, str]]:
        return [{"id": k, "file": v} for k, v in TOPIC_FILES.items()]

    @app.get("/api/topics/{topic_id}")
    async def get_topic(topic_id: str) -> dict[str, str]:
        filename = TOPIC_FILES.get(topic_id)
        if not filename:
            raise HTTPException(status_code=404, detail=f"Unknown topic: {topic_id}")
        path = ROOT / filename
        if not path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
        return {"id": topic_id, "file": filename, "content": path.read_text(encoding="utf-8")}

    return app


app = create_app()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve Interview Handbook preview")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
