from __future__ import annotations as _annotations

import os

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def wrap_in_page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    user_name = os.getenv("FASTUI_BLOG_USER_NAME")
    return [
        c.PageTitle(text=f"{user_name}'s Blog — {title}" if title else "Home"),
        c.Navbar(
            title=user_name,
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="About")],
                    on_click=GoToEvent(url="/about"),
                    active="startswith:/about",
                ),
                c.Link(
                    components=[c.Text(text="Posts")],
                    on_click=GoToEvent(url="/posts"),
                    active="startswith:/posts",
                ),
                c.Link(
                    components=[c.Text(text="GitHub")],
                    on_click=GoToEvent(url="https://github.com/kwon-evan/"),
                    active="startswith:/github",
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text=f"© 2024 {user_name}. All rights reserved.",
            links=[],
        ),
    ]


def read_md(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
