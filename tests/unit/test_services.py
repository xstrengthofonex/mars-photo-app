import json

import pytest

from mars_photo.http_client import HTTPClientTimeout, Response
from mars_photo.services import MarsPhotoService, GetPhotosRequest, ServiceUnavailable, InvalidGetPhotosRequest


async def test_calls_http_get_with_correct_query(mock_http_client):
    service = MarsPhotoService(mock_http_client)
    request = GetPhotosRequest(sol="100", camera="fhac", page="2")
    await service.get_photos(request)
    mock_http_client.get.assert_called_with(
        "https://mars-photos.herokuapp.com/api/v1/rovers/curiosity/photos?sol=100&page=2&camera=fhac")


async def test_raises_service_time_out_if_client_times_out(mock_http_client):
    with pytest.raises(ServiceUnavailable):
        mock_http_client.get.side_effect = HTTPClientTimeout
        service = MarsPhotoService(mock_http_client)
        await service.get_photos(GetPhotosRequest())


async def test_service_handles_json_response(mock_http_client):
    expected_result = dict(photos=[dict(img_src="some photo")])
    mock_http_client.get.return_value = Response(json.dumps(expected_result), 200, "application/json")
    service = MarsPhotoService(mock_http_client)
    request = GetPhotosRequest(sol="100", camera="fhac", page="2")
    photos = await service.get_photos(request)
    assert photos[0].get("src") == "some photo"


async def test_service_raises_invalid_get_photos_request_error(mock_http_client):
    service = MarsPhotoService(mock_http_client)
    with pytest.raises(InvalidGetPhotosRequest):
        request = GetPhotosRequest(sol="10000000000000000")
        await service.get_photos(request)
