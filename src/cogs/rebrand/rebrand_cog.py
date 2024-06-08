import asyncio
from datetime import datetime as dt

import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext.commands import Bot

from config import BOT_CHAT_ID, TIME_ZONE
from src.cogs.base import BaseCog
from src.cogs.rebrand.rebrand_users import USERS_ID
from src.utils.emoji_utils import get_random_sticker, get_random_formatted_emoji
from src.utils.role_utils import get_all_users_with_role, get_role_by_name


class Rebrand(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.users_id = USERS_ID
        self.remember_rebranding.start()

    @app_commands.command(description='Отобразить порядок ребрендинга')
    async def rebranding(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.guild.name,
                              color=discord.Color.random())
        now_user = get_all_users_with_role(interaction.guild, 'Ребрендинг')[0]
        next_user_place = self.users_id.index(now_user.id) + 1
        if next_user_place >= len(self.users_id):
            next_user_place = 0
        for player_id in self.users_id:
            user = interaction.guild.get_member(player_id)
            embed.add_field(name='', value=user.display_name, inline=False)
        embed.set_author(name=f'Сейчас: {now_user.display_name}',
                         icon_url=now_user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_image(url=interaction.guild.banner)
        next_user = interaction.guild.get_member(
            self.users_id[next_user_place])
        embed.set_footer(text=f'Следующий: {next_user.display_name}',
                         icon_url=next_user.avatar)
        await interaction.response.send_message(embed=embed)

    @tasks.loop(hours=168)
    async def remember_rebranding(self):
        channel = self.bot.get_channel(BOT_CHAT_ID)
        now_user = get_all_users_with_role(channel.guild, 'Ребрендинг')[0]
        next_user_place = self.users_id.index(now_user.id) + 1
        if next_user_place >= len(self.users_id):
            next_user_place = 0
        next_user = channel.guild.get_member(self.users_id[next_user_place])
        random_emoji = get_random_formatted_emoji(channel.guild)
        role = get_role_by_name(channel.guild, 'Ребрендинг')
        await now_user.remove_roles(role)
        await next_user.add_roles(role)
        await channel.send(f'<@{next_user.id}>, напоминаю, что сегодня ты делаешь Ребрендинг {random_emoji}')
        await channel.send(stickers=[get_random_sticker(channel.guild)])

    @remember_rebranding.before_loop
    async def before_remember(self):
        for _ in range(60 * 60 * 24 * 7 * 2):
            if dt.now(tz=TIME_ZONE).strftime("%H:%M UTC %a") == "00:01 UTC Fri":
                print('It is time for rebranding remembering')
                return

            await asyncio.sleep(30)
