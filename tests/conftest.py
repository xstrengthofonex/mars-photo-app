import os

import pytest
from aiohttp import web
from arsenic import start_session, services, browsers, stop_session

from mars_photo.app import create_app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_FILENAME = "chromedriver.exe"
CHROME_DRIVER_PATH = os.path.join(ROOT_DIR, CHROME_DRIVER_FILENAME)
HOST, PORT = "localhost", 4321
SERVER_ADDRESS = f"http://{HOST}:{PORT}"


@pytest.fixture
def app():
    return create_app()


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
