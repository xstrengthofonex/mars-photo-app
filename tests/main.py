from aiohttp import web

from mars_photo.app import create_app
from mars_photo.services import ServiceTimeout


class FakeService:
    @staticmethod
    async def get_photos(sol, camera):
        if sol == "1000":
            return [
                dict(src="http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol"
                         "/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG"),
                dict(src="http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol"
                         "/01000/opgs/edr/fcam/FRB_486265257EDR_F0481570FHAZ00323M_.JPG")]
        raise ServiceTimeout("API Timed out")


if __name__ == '__main__':
    web.run_app(create_app(FakeService()), port=3000)
