
import aiohttp

STEAM_API_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"


class SteamClientError(Exception):
    pass


class SteamClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = aiohttp.ClientSession()

    async def get_owned_games(self, steam_id: str) -> list[dict]:
        """Получить список игр пользователя Steam."""
        params = {"key": self.api_key, "steamid": steam_id, "include_appinfo": 1, "include_played_free_games": 0}

        async with self.session.get(STEAM_API_URL, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise SteamClientError(f"Steam API error {resp.status}: {text}")

            data = await resp.json()
            return data.get("response", {}).get("games", [])

    async def get_random_game_from_user(self, steam_id: str) -> dict | None:
        """Получить случайную игру из библиотеки пользователя."""

        games = await self.get_owned_games(steam_id)

        if not games:
            return None

        # Выбираем случайную игру
        import random

        return random.choice(games)

    async def close(self):
        """Закрыть сессию."""
        await self.session.close()
