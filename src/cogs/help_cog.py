import discord
from discord import app_commands


from src.cogs.base import BaseCog


class Help(BaseCog):
    @app_commands.command(description='Обычное приветствие')
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Привет, {interaction.user.display_name}!')
