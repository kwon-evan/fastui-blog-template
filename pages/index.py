import os

from fastapi import APIRouter
from fastui import FastUI, AnyComponent, components as c

from .shared import wrap_in_page, read_md

router = APIRouter()


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    avatar = os.getenv("FASTUI_BLOG_AVATAR_URL")
    return wrap_in_page(
        c.Div(
            components=[
                c.Div(
                    components=[
                        c.Image(
                            src=avatar
                            or "https://avatars.githubusercontent.com/u/11111111?v=4",
                            width=200,
                            height=200,
                            alt="Pydantic Logo",
                            loading="lazy",
                            referrer_policy="no-referrer",
                            class_name="border rounded",
                        ),
                    ],
                    class_name="col-md-auto",
                ),
                c.Div(
                    components=[
                        c.Markdown(text=read_md("./content/index.md")),
                    ],
                    class_name="col",
                ),
            ],
            class_name="row border-bottom mb-3 p-3",
        ),
        title="Home",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
