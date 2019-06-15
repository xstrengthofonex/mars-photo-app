import asyncio

IMAGE_SRCS = [
 "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol"
 "/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG",
 "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol"
 "/01000/opgs/edr/fcam/FRB_486265257EDR_F0481570FHAZ00323M_.JPG"
]


async def test_should_find_photos_given_valid_input(session):
    await session.get("/")
    sol_input = await session.get_element("#sol_input")
    await sol_input.send_keys("1000")
    camera_input = await session.get_element("#camera_input")
    await camera_input.send_keys("fhaz")
    submit_btn = await session.get_element("#submit_btn")
    await submit_btn.click()
    await asyncio.sleep(2)

    photos = await session.get_elements(".photo")
    assert 2 == len(photos)
    for photo in photos:
        assert await photo.get_attribute("src") in IMAGE_SRCS
