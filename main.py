from __future__ import annotations as _annotations

import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastui import prebuilt_html
from fastui.dev import dev_fastapi_app
from httpx import AsyncClient
from dotenv import load_dotenv

from pages.index import router as index_router
from pages.about import router as about_router
from pages.posts import router as posts_router

load_dotenv()


@asynccontextmanager
async def lifespan(app_: FastAPI):
    async with AsyncClient() as client:
        app_.state.httpx_client = client
        yield


frontend_reload = "--reload" in sys.argv
if frontend_reload:
    app = dev_fastapi_app(lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan)


app.include_router(posts_router, prefix="/api/posts")
app.include_router(about_router, prefix="/api/about")
app.include_router(index_router, prefix="/api")


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt() -> str:
    return "User-agent: *\nAllow: /"


@app.get("/favicon.ico", status_code=404, response_class=PlainTextResponse)
async def favicon_ico() -> str:
    return "page not found"


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    return HTMLResponse(
        prebuilt_html(title=f"{os.getenv('FASTUI_BLOG_USER_NAME')}'s Blog")
    )
