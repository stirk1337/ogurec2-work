import httpx

from config import TENOR_API_KEY

LIMIT = 1


async def get_first_tenor_gif_url(search: str) -> str:
    async with httpx.AsyncClient() as client:
        tenor_url = f'https://tenor.googleapis.com/v2/search?q={search}&key={TENOR_API_KEY}&limit={LIMIT}'
        print(tenor_url)
        response = await client.get(tenor_url)
 #       url = response.json()['results'][0]['media'][0]['mediumgif']['url']
#        return url
        return response.json()["results"][0]["media_formats"]["mediumgif"]["url"]
