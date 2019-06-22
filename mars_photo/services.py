from dataclasses import dataclass
from typing import List, Dict

from yarl import URL

from mars_photo.http_client import HTTPClientTimeout


class ServiceUnavailable(RuntimeError):
    pass


class InvalidGetPhotosRequest(RuntimeError):
    pass


@dataclass(frozen=True)
class GetPhotosRequest:
    sol: str = ""
    page: str = ""
    camera: str = ""


class MarsPhotoService:
    def __init__(self, http_client):
        self.http_client = http_client

    async def get_photos(self, request: GetPhotosRequest) -> List[Dict[str, str]]:
        self.validate_request(request)
        try:
            response = await self.http_client.get(self.create_url_from_request(request))
            data = response.json()
            results = [dict(src=photo.get("img_src")) for photo in data.get("photos")]
            return results
        except HTTPClientTimeout:
            raise ServiceUnavailable

    @staticmethod
    def create_url_from_request(request):
        url = URL("https://mars-photos.herokuapp.com/api/v1/rovers/curiosity/photos")
        url = url.update_query(dict(sol=request.sol, page=request.page))
        if request.camera:
            url = url.update_query(dict(camera=request.camera))
        return str(url)

    @staticmethod
    def validate_request(request):
        if request.sol.isnumeric():
            sol_int = int(request.sol)
            if sol_int < 0 or sol_int > 2000:
                raise InvalidGetPhotosRequest
