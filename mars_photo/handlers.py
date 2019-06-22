import os

from aiohttp import web

import settings
from mars_photo.services import ServiceUnavailable, GetPhotosRequest, InvalidGetPhotosRequest


async def index_handler(request):
    return web.FileResponse(os.path.join(settings.STATIC_DIR, "index.html"))


async def photos_handler(request: web.Request):
    services = request.app.get("service")
    get_photos_request = GetPhotosRequest(
        sol=request.rel_url.query.get("sol", ""),
        camera=request.rel_url.query.get("camera", ""),
        page=request.rel_url.query.get("page", "1"))
    try:
        photos = await services.get_photos(get_photos_request)
    except InvalidGetPhotosRequest as e:
        photos = []
    except ServiceUnavailable as e:
        return web.json_response(dict(errors=e.args), status=408)
    return web.json_response(photos)
