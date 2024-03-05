from glob import glob
from datetime import datetime

from fastapi import APIRouter
from fastui import FastUI, AnyComponent, components as c
from fastui.events import GoToEvent
from pydantic import BaseModel
import frontmatter

from .shared import wrap_in_page

router = APIRouter()


class PostModel(BaseModel):
    title: str
    date: datetime | None = None
    category: list[str] | None = None
    content: str


def parse_mdx(post_path: str) -> PostModel:
    with open(post_path) as f:
        metadata, content = frontmatter.parse(f.read())

    return PostModel(
        title=metadata.get("title", "Untitled"),
        date=metadata.get("date", None),
        category=metadata.get("category", None),
        content=content,
    )


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    posts_path = "./contents/posts"
    posts_list = glob(posts_path + "/*.md*")
    posts = [parse_mdx(post_path) for post_path in posts_list]

    return wrap_in_page(
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text=post.title),
                        c.Markdown(text=post.content),
                    ],
                    class_name="border-bottom mt-3 pt-1",
                )
                for post in posts
            ]
        ),
        title="Post",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
