# -*- coding: utf-8 -*-
from pathlib import Path

from litestar import Litestar, Request, get, post
from litestar.config.cors import CORSConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from missions import MissionGatherer
from notification import send_notification

cors_config = CORSConfig(allow_origins=["*"])
ASSETS_DIR = Path("assets")


def initialization():
    global mission_gatherer
    mission_gatherer = MissionGatherer()


@post("/send_report")
async def send_report(request: Request) -> None:
    form_data = await request.form()
    username = form_data.get("report_author", None)
    content = form_data.get("report_content", None)
    if not username:
        username = "Anonymous"
    if content:
        send_notification(username, content)


@get("/")
async def index(request: Request) -> Template:
    entry_point = request.query_params.get(
        "entry_point", f"http://{request.headers.get('host')}"
    )
    language = request.query_params.get("language", "en")
    if language == "en":
        from translations.website.english import (
            BOOKS,
            DIFFICULTIES,
            EVENT_FILTERS,
            FILTERS,
            MAPS,
            UI_TRANSLATIONS,
        )

    elif language == "zh-tw":
        from translations.website.traditional_chinese import (
            BOOKS,
            DIFFICULTIES,
            EVENT_FILTERS,
            FILTERS,
            MAPS,
            UI_TRANSLATIONS,
        )

    elif language == "zh-cn":
        from translations.website.simplified_chinese import (
            BOOKS,
            DIFFICULTIES,
            EVENT_FILTERS,
            FILTERS,
            MAPS,
            UI_TRANSLATIONS,
        )

    context = {
        "server_entry_point": entry_point.strip("/"),
        "language": language,
        "ui_translations": UI_TRANSLATIONS,
        "difficulties": DIFFICULTIES,
        "filters": FILTERS,
        "event_filters": EVENT_FILTERS,
        "maps": MAPS,
        "books": BOOKS,
    }
    return Template(template_name="index.html", context=context)


@post("/get_missions")
async def get_missions(request: Request) -> Template:
    if request.headers.get("hx-request", None) == "true":
        form_data = await request.form()
        language = form_data.get("language", "en")

        if language == "zh-tw":
            mission_gatherer.language = "zh-tw"
            from translations.website.traditional_chinese import (
                FILTERS,
                UI_TRANSLATIONS,
            )

        elif language == "zh-cn":
            mission_gatherer.language = "zh-cn"
            from translations.website.simplified_chinese import FILTERS, UI_TRANSLATIONS

        else:
            mission_gatherer.language = "en"
            from translations.website.english import FILTERS, UI_TRANSLATIONS

        filter_keywords = [
            key
            for key in form_data
            if key != "language"
            and key != "auric_only"
            and key != "auric_maelstrom_only"
            and key != "entry_point"
        ]
        mission_gatherer.filter_keywords = filter_keywords
        if form_data.get("auric_maelstrom_only", "false") == "on":
            auric_maelstrom_only = True
            mission_gatherer.filter_keywords.append(FILTERS["Hi-Intensity"])
        else:
            auric_maelstrom_only = False
        mission_data = mission_gatherer.get_requested_missions(
            auric_maelstrom_only=auric_maelstrom_only
        )
        if form_data.get("auric_only", "false") == "on":
            mission_data = [
                mission for mission in mission_data if mission["is_auric"] is True
            ]
        context = {
            "missions": mission_data,
            "ui_translations": UI_TRANSLATIONS,
            "server_entry_point": form_data.get("entry_point", ""),
        }
        return Template(template_name="mission.html", context=context)


app = Litestar(
    [
        index,
        get_missions,
        create_static_files_router(path="/assets", directories=[ASSETS_DIR]),
        send_report,
    ],
    template_config=TemplateConfig(directory="templates", engine=JinjaTemplateEngine),
    cors_config=cors_config,
    on_startup=[initialization],
)
