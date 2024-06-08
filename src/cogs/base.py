from discord.ext import commands
from discord.ext.commands import Bot


class BaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
