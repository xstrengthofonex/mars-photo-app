import json

import aiohttp


class HTTPClientTimeout(RuntimeError):
    pass


class Response:
    def __init__(self, body: str, status: int, content_type: str):
        self.body = body
        self.status = status
        self.content_type = content_type

    def json(self):
        return json.loads(self.body)


class HTTPClient:
    async def get(self, url: str) -> Response:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = Response(
                        body=await response.text(),
                        status=response.status,
                        content_type=response.content_type)
            return response
        except aiohttp.ClientTimeout:
            raise HTTPClientTimeout
