import discord
from discord.ext import commands
from loguru import logger

from src.config.settings import Settings


class OgurecBot(commands.Bot):
    def __init__(self, settings: Settings):
        self.settings = settings

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=settings.prefix,
            intents=intents,
        )

    async def on_ready(self):
        print('123')
        logger.info(f"We have logged in as {self.user}")
