from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def wrap_in_page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"Kwon Evan's Blog — {title}" if title else "Home"),
        c.Navbar(
            title="Kwon Evan",
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
                *components,
            ],
        ),
        c.Footer(
            extra_text="© 2024 Kwon Evan. All rights reserved.",
            links=[],
        ),
    ]
