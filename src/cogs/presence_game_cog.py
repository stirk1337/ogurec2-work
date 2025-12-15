import random

import discord
from discord.ext import commands, tasks

from src.bot import OgurecBot
from src.tenor import TenorClient

GAME_POST_GUARANTEE = 5


class PresenceGameCog(commands.Cog):
    def __init__(self, bot: OgurecBot, tenor_client: TenorClient):
        self.bot = bot
        self.tenor_client = tenor_client

        self.game_post_counter = 0

        self.statuses = (
            discord.Status.online,
            discord.Status.idle,
            discord.Status.dnd,
        )

        self.update_presence.start()

    @tasks.loop(hours=1)
    async def update_presence(self):
        channel = self.bot.get_channel(self.bot.settings.main_chat_id)
        if not channel:
            return

        game_name = "game"  # TODO: Steam API
        activity = discord.Game(name=game_name)

        await self.bot.change_presence(
            status=random.choice(self.statuses),
            activity=activity,
        )

        self.game_post_counter += 1
        trigger = random.randint(1, 50) == 10 or self.game_post_counter >= GAME_POST_GUARANTEE

        if trigger:
            await channel.send(f"Жёстко иду играть в {game_name}")
            gif_url = await self.tenor_client.get_first_gif_url(game_name)
            await channel.send(gif_url)
            self.game_post_counter = 0
