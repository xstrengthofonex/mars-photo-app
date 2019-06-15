import os


from aiohttp import web

import settings
from mars_photo.services import ServiceTimeout


async def index_handler(request):
    return web.FileResponse(os.path.join(settings.STATIC_DIR, "index.html"))


async def photos_handler(request: web.Request):
    services = request.app.get("services")
    sol = request.rel_url.query.get("sol")
    camera = request.rel_url.query.get("camera")
    try:
        photos = await services.get_photos(sol=sol, camera=camera)
    except ServiceTimeout as e:
        return web.json_response(dict(errors=e.args), status=408)
    return web.json_response(photos)
