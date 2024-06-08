import httpx

from config import TENOR_API_KEY

LIMIT = 1


async def get_first_tenor_gif_url(search: str) -> str:
    async with httpx.AsyncClient() as client:
        tenor_url = f'https://g.tenor.com/v1/search?q={search}&key={TENOR_API_KEY}&limit={LIMIT}'
        response = await client.get(tenor_url)
        url = response.json()['results'][0]['media'][0]['mediumgif']['url']
        return url
