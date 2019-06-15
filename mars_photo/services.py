from typing import List, Dict

import aiohttp
from yarl import URL


class ServiceTimeout(RuntimeError):
    pass


async def get_photos(sol: str, camera: str, page: str) -> List[Dict[str, str]]:
    url = URL("https://mars-photos.herokuapp.com/api/v1/rovers/curiosity/photos")
    url = url.update_query(dict(sol=sol, page=page))
    if camera:
        url = url.update_query(dict(camera=camera))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            results = [dict(src=photo.get("img_src")) for photo in data.get("photos")]
    return results
