from glob import glob
from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastui import FastUI, AnyComponent, components as c
from fastui.events import GoToEvent
from pydantic import BaseModel, Field
import frontmatter

from .shared import wrap_in_page

router = APIRouter()


class PostModel(BaseModel):
    file_name: str
    title: str
    postdate: date = Field(default_factory=date.today)
    tags: Optional[list[str]]
    content: str


def parse_mdx(post_path: str) -> PostModel:
    with open(post_path) as f:
        metadata, content = frontmatter.parse(f.read())

    # FIXME: fix type error
    return PostModel(
        file_name=post_path.split("/")[-1],
        title=metadata.get("title", "Untitled"),
        postdate=metadata.get("date", None),
        tags=metadata.get("tags", None),
        content=content,
    )


def read_posts(path: str) -> list[PostModel]:
    return sorted(
        [parse_mdx(post_path) for post_path in glob(path + "/*.md*")],
        key=lambda post: post.postdate,
    )


def post_item(post: PostModel) -> AnyComponent:
    return c.Div(
        components=[
            c.Link(
                components=[c.Heading(text=post.title, level=4)],
                on_click=GoToEvent(url=f"{post.file_name}"),
                class_name="text-decoration-none text-dark",
            ),
            c.Paragraph(
                text=" ".join(list(map(lambda tag: f"#{tag}", post.tags or []))),
                class_name="text-muted mb-0 pb-0",
            ),
            c.Paragraph(
                text=post.postdate.strftime("%Y/%m/%d"),
                class_name="text-muted",
            ),
        ],
        class_name="border-bottom mb-3",
    )


posts = read_posts("./content/posts")


@router.get("/{file_name}", response_model=FastUI, response_model_exclude_none=True)
def post_page(file_name: str) -> list[AnyComponent]:
    try:
        post = next(filter(lambda post: post.file_name == file_name, posts))
    except StopIteration:
        raise HTTPException(status_code=404, detail="Post not found")

    return wrap_in_page(
        c.Page(
            components=[
                c.Paragraph(
                    text=", ".join(post.tags or []),
                    class_name="text-muted",
                ),
                c.Paragraph(
                    text=post.postdate.strftime("%Y/%m/%d"),
                    class_name="text-muted border-bottom pb-3 mb-3",
                ),
                c.Markdown(text=post.content),
            ],
        ),
        title=post.title,
    )


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    return wrap_in_page(
        c.Page(
            components=list(map(post_item, posts)),
        ),
        title="Posts",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
