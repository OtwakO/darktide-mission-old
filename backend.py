# -*- coding: utf-8 -*-
from litestar import Litestar, Request, get, post
from litestar.config.cors import CORSConfig

# from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig

from missions import MissionGatherer

cors_config = CORSConfig(allow_origins=["*"])


def initialization():
    global mission_gatherer
    mission_gatherer = MissionGatherer()


@get("/")
async def index(request: Request) -> Template:
    entry_point = request.query_params.get(
        "entry_point", f"http://{request.headers.get('host')}"
    )
    language = request.query_params.get("language", "en")
    if language == "en":
        from translations.website.english import DIFFICULTIES, FILTERS, UI_TRANSLATIONS

    elif language == "zh-tw":
        from translations.website.traditional_chinese import (
            DIFFICULTIES,
            FILTERS,
            UI_TRANSLATIONS,
        )

    context = {
        "server_entry_point": entry_point,
        "language": language,
        "ui_translations": UI_TRANSLATIONS,
        "difficulties": DIFFICULTIES,
        "filters": FILTERS,
    }
    return Template(template_name="index.html", context=context)


@post("/get_missions")
async def get_missions(request: Request) -> Template:
    if request.headers.get("hx-request", None) == "true":
        form_data = await request.form()
        language = form_data.get("language", "en")

        if language == "zh-tw":
            mission_gatherer.language = "zh-tw"
            from translations.website.traditional_chinese import UI_TRANSLATIONS

        else:
            mission_gatherer.language = "en"
            from translations.website.english import UI_TRANSLATIONS

        filter_keywords = [
            key
            for key in form_data
            if key != "language" and key != "auric_maelstrom_only"
        ]
        mission_gatherer.filter_keywords = filter_keywords
        if form_data.get("auric_maelstrom_only", "false") == "on":
            auric_maelstrom_only = True
        else:
            auric_maelstrom_only = False
        mission_data = mission_gatherer.get_requested_missions(
            auric_maelstrom_only=auric_maelstrom_only
        )
        context = {
            "missions": mission_data,
            "ui_translations": UI_TRANSLATIONS,
        }
        return Template(template_name="mission.html", context=context)


app = Litestar(
    [index, get_missions],
    template_config=TemplateConfig(directory="templates", engine=JinjaTemplateEngine),
    cors_config=cors_config,
    on_startup=[initialization],
)
