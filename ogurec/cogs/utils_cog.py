from datetime import datetime as dt

from discord.ext import commands

from ogurec.utils import TIME_ZONE


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    async def sync(self, ctx: commands.Context):
        synced = await self.bot.tree.sync()
        await ctx.send(f"Синхронизировано {len(synced)} команд.")

    @commands.command(name="time")
    async def time(self, ctx: commands.Context):
        now = dt.now(tz=TIME_ZONE)
        week = now.isocalendar()[1]
        await ctx.send(now.strftime("%H:%M UTC %a") + f" week {week}")
