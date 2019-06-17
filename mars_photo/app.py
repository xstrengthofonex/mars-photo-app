from mimetypes import add_type

from aiohttp import web

import settings
from mars_photo import handlers

add_type("application/javascript", ".js", True)


def create_app(service):
    app = web.Application()
    app["service"] = service
    app.router.add_get("/api/photos", handlers.photos_handler)
    app.router.add_get("/", handlers.index_handler)
    app.router.add_static("/static", settings.STATIC_DIR)
    return app


