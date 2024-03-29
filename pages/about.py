from fastapi import APIRouter
from fastui import FastUI, AnyComponent, components as c

from .shared import wrap_in_page, read_md

router = APIRouter()


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    return wrap_in_page(
        c.Page(
            components=[
                c.Markdown(text=read_md("./content/about.md")),
            ]
        ),
        title="About",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
