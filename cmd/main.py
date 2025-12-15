import asyncio

from src.bot import OgurecBot
from src.chatgpt import GPTClient
from src.cogs.help_cog import Help
from src.cogs.presence_game_cog import PresenceGameCog
from src.cogs.random_message_cog import RandomMessageCog
from src.cogs.rebrand.rebrand_cog import Rebrand
from src.cogs.utils_cog import Utils
from src.config.settings import Settings
from src.tenor import TenorClient


async def amain():
    settings = Settings()
    bot = OgurecBot(settings)

    tenor_client = TenorClient(settings.tenor_api_key)
    gpt_client = GPTClient(settings.gpt_api_key)

    await bot.add_cog(Utils(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Rebrand(bot))
    await bot.add_cog(RandomMessageCog(bot, gpt_client))
    await bot.add_cog(PresenceGameCog(bot, tenor_client))

    await bot.start(token=settings.discord_bot_token)


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
