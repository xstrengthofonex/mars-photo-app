import os

import pytest
from aiohttp import web
from arsenic import start_session, services, browsers, stop_session
from asynctest import Mock

from mars_photo.app import create_app
from mars_photo.http_client import HTTPClient
from mars_photo.services import MarsPhotoService


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_FILENAME = "chromedriver.exe"
CHROME_DRIVER_PATH = os.path.join(ROOT_DIR, CHROME_DRIVER_FILENAME)
HOST, PORT = "localhost", 4321
SERVER_ADDRESS = f"http://{HOST}:{PORT}"


@pytest.fixture
def mock_http_client():
    return Mock(HTTPClient)


@pytest.fixture
def mock_service():
    return Mock(MarsPhotoService)


@pytest.fixture
def app(mock_service):
    return create_app(service=mock_service)


@pytest.fixture
def client(loop, app, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
async def server(app, loop):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    try:
        yield await site.start()
    finally:
        await site.stop()


@pytest.fixture
async def session(server):
    session = await start_session(
        services.Chromedriver(binary=CHROME_DRIVER_PATH),
        browsers.Chrome(chromeOptions={'args': ['--headless', '--disable-gpu']}),
        bind=SERVER_ADDRESS)
    try:
        yield session
    finally:
        await stop_session(session)
