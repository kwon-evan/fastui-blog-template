from glob import glob

from fastapi import APIRouter
from fastui import FastUI, AnyComponent, components as c

from .shared import wrap_in_page

router = APIRouter()


def get_posts(posts_path: str) -> list[str]:
    globbed = glob(f"{posts_path}/*.md")
    print(globbed)
    return globbed


def read_posts(posts_path: str, post_name: str) -> str:
    ret = ""
    with open(f"{posts_path}/{post_name}.md", "r") as f:
        ret = f.read()
    return ret


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def main_page() -> list[AnyComponent]:
    posts_path = "./posts"
    posts = get_posts(posts_path)
    post_titles = list(map(lambda path: path.split("/")[-1][:-3], posts))

    return wrap_in_page(
        c.Page(
            components=[
                c.Markdown(text=read_posts(posts_path, post_titles[0])),
            ]
        ),
        title="Post",
    )


@router.get("/{path:path}", status_code=404)
async def api_404():
    return {"message": "Not found"}
