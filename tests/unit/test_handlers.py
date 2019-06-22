from mars_photo.services import ServiceUnavailable, GetPhotosRequest, InvalidGetPhotosRequest


async def test_should_get_photos_should_be_called_with_correct_args(client, mock_service):
    request = GetPhotosRequest(sol="100", camera="fhac", page="2")
    mock_service.get_photos.return_value = []
    await client.get("/api/photos?sol=100&camera=fhac&page=2")
    mock_service.get_photos.assert_called_with(request)


async def test_should_return_a_list_of_photo_entries(client, mock_service):
    photos = [dict(src="photo1"), dict(src="photo2")]
    mock_service.get_photos.return_value = photos
    response = await client.get("/api/photos")
    assert response.status == 200
    assert response.content_type == "application/json"
    body = await response.json()
    assert photos == body


async def test_should_return_408_if_the_client_times_out(client, mock_service):
    error_message = "Client timed out"
    mock_service.get_photos.side_effect = ServiceUnavailable(error_message)
    response = await client.get("/api/photos")
    assert response.status == 408
    assert response.content_type == "application/json"
    body = await response.json()
    assert error_message in body.get("errors")


async def test_should_return_blank_list_if_request_data_is_invalid(client, mock_service):
    mock_service.get_photos.side_effect = InvalidGetPhotosRequest
    response = await client.get("api/photos?sol=100000000000000000")
    assert response.status == 200
    assert response.content_type == "application/json"
    body = await response.json()
    assert body == []
