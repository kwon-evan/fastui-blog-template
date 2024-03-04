from fastapi import APIRouter
from fastui import FastUI, AnyComponent, components as c

from .shared import wrap_in_page

router = APIRouter()

welcome_prompt = """


**Greetings!**  

I'm Heonjin Kwon, an ML engineer.  

"""


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    return wrap_in_page(
        c.Image(
            src="https://avatars.githubusercontent.com/u/87924725?v=4",
            alt="Pydantic Logo",
            width=200,
            height=200,
            loading="lazy",
            referrer_policy="no-referrer",
            class_name="border rounded",
        ),
        c.Paragraph(text=""),
        c.Markdown(text=welcome_prompt),
        title="Home",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
