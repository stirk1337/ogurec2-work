import aiohttp

TENOR_API_URL = "https://tenor.googleapis.com/v2/search"


class TenorClientError(Exception):
    pass


class TenorClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = aiohttp.ClientSession()

    async def get_first_gif_url(self, query: str) -> str:
        params = {
            "q": query,
            "key": self.api_key,
            "limit": 1,
        }

        async with self.session.get(TENOR_API_URL, params=params) as resp:
            if resp.status != 200:
                raise TenorClientError(f"Tenor API error: {resp.status}")

            data = await resp.json()

        try:
            return data["results"][0]["media_formats"]["mediumgif"]["url"]
        except (KeyError, IndexError) as e:
            raise TenorClientError("GIF not found") from e
