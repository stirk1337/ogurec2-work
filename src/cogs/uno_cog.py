import asyncio
from datetime import datetime as dt
import datetime
from random import shuffle

import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext.commands import Bot

from config import TIME_ZONE, BOT_CHAT_ID
from src.cogs.base import BaseCog
from src.google_docs.google_docs import get_table
from src.utils.emoji_utils import get_random_formatted_emoji, get_random_sticker
from src.utils.role_utils import get_all_users_with_role, get_role_by_name

UNO_LOGO_URL = ('https://media.discordapp.net/attachments/1043248714652860477/1206889284242772019'
                '/1740671508_preview_1280px-UNO_Logo_svg.png?ex=65dda63c&is=65cb313c&hm'
                '=63bf1c5c79afd8c3a14f9b9c528a23cd0a50d308cfc1a6df69725ba7c6ef6be7&=&format=webp&quality=lossless'
                '&width=833&height=585')

GOOGLE_SPREADSHEETS_LOGO_URL = ('https://media.discordapp.net/attachments/1043248714652860477/1206901181079748618'
                                '/be52957fc0b0ec8.webp?ex=65ddb150&is=65cb3c50&hm'
                                '=81f134804f73570f2409022106c6b367ca4045418234c625003ef16f0399dc44&=&format=webp'
                                '&width=585&height=585')

UNO_TIME = datetime.time(hour=19, minute=47, tzinfo=TIME_ZONE)


class Uno(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.remember_uno.start()

    @app_commands.command(description='Отобразить таблицу UNO из Google Таблицы')
    async def uno(self, interaction: discord.Interaction):
        values = get_table()['values']
        embed = discord.Embed(title='Результаты UNO',
                              color=discord.Color.random(),
                              timestamp=datetime.datetime.now())
        embed.set_author(name=interaction.user.display_name,
                         icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=UNO_LOGO_URL)
        embed.set_footer(text="Google Таблицы",
                         icon_url=GOOGLE_SPREADSHEETS_LOGO_URL)
        for score in values[1:7]:
            embed.add_field(name=f'**{score[0]}**',
                            value=f'> Шансㅤ \t{score[1]}\n> Победы {score[2]}\n> Лузы ㅤ\t{score[3]}',
                            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Случайный порядок игроков с ролью UNO')
    async def uno_shuffle(self, interaction: discord.Interaction):
        uno_players = get_all_users_with_role(interaction.guild, 'Uno')
        shuffle(uno_players)
        embed = discord.Embed(title='UNO Шаффл!',
                              color=discord.Color.random())
        embed.set_thumbnail(url=UNO_LOGO_URL)
        for player in uno_players:
            embed.add_field(name='', value=player.display_name, inline=False)
        await interaction.response.send_message(embed=embed)

    @tasks.loop(hours=336)
    async def remember_uno(self):
        channel = self.bot.get_channel(BOT_CHAT_ID)
        role = get_role_by_name(channel.guild, 'Uno')
        await channel.send(f'<@&{role.id}>, напоминаю, что сегодня UNO {get_random_formatted_emoji(channel.guild)}')
        await channel.send(stickers=[get_random_sticker(channel.guild)])

    @remember_uno.before_loop
    async def before_remember(self):
        for _ in range(60 * 60 * 24 * 7 * 2):
            if dt.now(tz=TIME_ZONE).strftime("%H:%M UTC %a") == "12:00 UTC Sat" and \
                    dt.now(tz=TIME_ZONE).isocalendar()[1] % 2 == 0:
                print('It is time for uno remembering')
                return

            await asyncio.sleep(30)
