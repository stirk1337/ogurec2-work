import asyncio
from datetime import datetime as dt

import discord
from discord.ext.commands import Bot

from config import TOKEN, TIME_ZONE
from src.cogs.fun.fun_cog import Fun
from src.cogs.fun.pyrogram.pyro_bot import app
from src.cogs.help_cog import Help
from src.cogs.rebrand.rebrand_cog import Rebrand
from src.cogs.uno_cog import Uno

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(Uno(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Rebrand(bot))
    print(f'We have logged in as {bot.user}')


@bot.command(name="sync")
async def sync(ctx):
    synced = await bot.tree.sync()
    await ctx.send(f"Синхронизировано {len(synced)} команд.")


@bot.command(name="time")
async def time(ctx):
    await ctx.send(dt.now(tz=TIME_ZONE).strftime("%H:%M UTC %a") + f' week {dt.now(tz=TIME_ZONE).isocalendar()[1]}')


async def start_bots():
    await asyncio.gather(
        bot.start(TOKEN),
        app.start()
    )
    print('Both bots started successfully')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bots())
