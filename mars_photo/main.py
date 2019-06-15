from aiohttp import web

from mars_photo import services
from mars_photo.app import create_app

if __name__ == '__main__':
    web.run_app(create_app(services=services), port=3000)
