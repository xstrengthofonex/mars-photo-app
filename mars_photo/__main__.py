from aiohttp import web

import settings
from mars_photo.app import create_app
from mars_photo.http_client import HTTPClient
from mars_photo.services import MarsPhotoService


service = MarsPhotoService(HTTPClient())
web.run_app(create_app(service=service), port=settings.PORT)
