import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Обычное приветствие")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Привет, {interaction.user.display_name}!")
