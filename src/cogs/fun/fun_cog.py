import asyncio
import json
import random
import enum
from typing import List

import discord
from discord import app_commands, Message
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from config import MAIN_CHAT_ID
from src.cogs.base import BaseCog
from src.cogs.fun.banwords import BAN_WORDS, POOP_EMOJIS
from src.cogs.fun.eight_ball import EIGHT_BALL
from src.cogs.fun.game_reviews import GAME_REVIEWS
from src.cogs.fun.games_list import GAMES
from src.cogs.fun.pyrogram.pyro_bot import send_gpt_message, gpt_stack
from src.tenor.tenor import get_first_tenor_gif_url
from src.utils.emoji_utils import get_random_formatted_emoji, get_random_sticker
from src.utils.mention_utils import remove_user_mentions


class GptStatus(enum.Enum):
    FREE = 'free'
    GENERATING = 'generating'


class Fun(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.on_message_counter = 0
        self.on_game_counter = 0
        self.ON_MESSAGE_GUARANTEE = 750
        self.ON_GAME_GUARANTEE = 5
        self.game_reviews = GAME_REVIEWS
        self.answers = EIGHT_BALL
        self.bot_play.start()
        self.reset_gpt_dialog_history.start()
        self.statuses = [
            discord.Status.online,
            discord.Status.idle,
            discord.Status.dnd,
        ]
        self.GAME_STATS_PATH_JSON = 'src/cogs/fun/game_stats.json'
        with open(self.GAME_STATS_PATH_JSON, 'r') as fp:
            self.game_stats = json.load(fp)

    async def answer_question(self, message: Message) -> bool:
        if self.bot.user.mentioned_in(message) and message.content[-1] in ['?', '.', '!']:
            async with message.channel.typing():
                await send_gpt_message(remove_user_mentions(message.content), use_moods=True)
                gpt_stack.append(message)
            return True
        return False

    async def send_random_phrase(self, message: Message) -> bool:
        random_number = random.randint(1, 450)
        if random_number in [1, 2]:
            async with message.channel.typing():
                await send_gpt_message(remove_user_mentions(message.content), use_moods=True)
                gpt_stack.append(message)
            return True
        return False

    async def answer_ping(self, message: Message):
        if self.bot.user.mentioned_in(message):
            async with message.channel.typing():
                await asyncio.sleep(random.randint(2, 6))
                random_number = random.randint(1, 4)
                if random_number == 1:  # 25%
                    await message.channel.send(stickers=[get_random_sticker(message.channel.guild)], reference=message)
                else:
                    formatted_emoji = get_random_formatted_emoji(
                        message.channel.guild)
                    await message.channel.send(formatted_emoji, reference=message)

    async def send_random_emoji(self, message: Message) -> bool:
        random_number = random.randint(1, 450)
        if random_number in [1, 2] or self.on_message_counter == self.ON_MESSAGE_GUARANTEE:
            if not self.bot.user.mentioned_in(message):
                self.on_message_counter = 0
            async with message.channel.typing():
                await asyncio.sleep(random.randint(2, 6))
                formatted_emoji = get_random_formatted_emoji(
                    message.channel.guild)
                await message.channel.send(formatted_emoji, reference=message)
            return True
        return False

    async def send_random_sticker(self, message: Message) -> bool:
        random_number = random.randint(1, 450)
        if random_number in [1, 2] or self.on_message_counter == self.ON_MESSAGE_GUARANTEE:
            if not self.bot.user.mentioned_in(message):
                self.on_message_counter = 0
            async with message.channel.typing():
                await asyncio.sleep(random.randint(2, 6))
                await message.channel.send(stickers=[get_random_sticker(message.channel.guild)], reference=message)
            return True
        return False

    async def set_random_reaction(self, message: Message):
        random_number = random.randint(1, 650)
        if 3 <= random_number <= 10:
            await asyncio.sleep(random.randint(1, 4))
            await message.add_reaction(random.choice(message.guild.emojis))

    async def poop_banword_message(self, message: Message):
        message_words = message.content.split()
        for message_word in message_words:
            for word in BAN_WORDS:
                if fuzz.ratio(word, message_word.lower()) > 80:
                    print(fuzz.ratio(word, message_word.lower()))
                    emojis = message.guild.emojis
                    filter_emojis = [emoji for emoji in emojis if emoji.name in POOP_EMOJIS]
                    await message.add_reaction(random.choice(filter_emojis))
                    return

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id in [self.bot.user.id]:
            return
        question = await self.answer_question(message)
        if question:
            return

        phrase = await self.send_random_phrase(message)
        if phrase:
            return

        ping = await self.answer_ping(message)
        if ping:
            return

        sticker = await self.send_random_sticker(message)
        if sticker:
            return

        emoji = await self.send_random_emoji(message)
        if emoji:
            return

        await self.poop_banword_message(message)

        await self.set_random_reaction(message)
        self.on_message_counter += 1

    @app_commands.command(description='Получить оценку игры. Примечание: я конченный')
    @app_commands.describe(game="Игра")
    async def rgame(self, interaction: discord.Interaction, game: str):
        await interaction.response.send_message(f'Запросили оценку {game}. Жёстко анализирую...')
        async with interaction.channel.typing():
            await asyncio.sleep(random.randint(1, 10))
            await interaction.followup.send(self.game_reviews[random.randint(0, len(self.game_reviews) - 1)])

    @tasks.loop(hours=1)
    async def bot_play(self):
        channel = self.bot.get_channel(MAIN_CHAT_ID)
        game = random.choice(GAMES)
        activity = discord.Game(name=game)
        await self.bot.change_presence(status=random.choice(self.statuses), activity=activity)
        random_number = random.randint(1, 50)
        if game not in self.game_stats:
            self.game_stats[game] = 0
        self.game_stats[game] += 1
        self.on_game_counter += 1
        with open(self.GAME_STATS_PATH_JSON, 'w') as fp:
            json.dump(self.game_stats, fp)
        if random_number == 10 or self.on_game_counter == self.ON_GAME_GUARANTEE:
            await channel.send(f'Жёстко иду играть в {game}')
            gif_url = await get_first_tenor_gif_url(game)
            print(gif_url)
            await channel.send(gif_url)
            self.on_game_counter = 0

    @tasks.loop(minutes=10)
    async def reset_gpt_dialog_history(self):
        from src.cogs.fun.pyrogram.pyro_bot import last_message
        print('Resetting dialog history')
        try:
            await last_message.click(0)
        except Exception as e:
            print('Error reset dialog history:', e)

    @app_commands.command(description='Мой профиль Steam (ну типа)')
    async def game_stats(self, interaction: discord.Interaction):
        embed_maximum_fields_count = 25
        steam_icon = ('https://media.discordapp.net/attachments/1043248714652860477/1209895513684578404/2048px'
                      '-Steam_icon_logo.png?ex=65e89601&is=65d62101&hm'
                      '=f55079bb3d466b9d8b53a377d780361c87b38ec2c0ccaad1decbbbc23f4e50c1&=&format=webp&quality'
                      '=lossless&width=590&height=590')
        games_count = min(len(self.game_stats), embed_maximum_fields_count)
        embed = discord.Embed(title=f"Мой топ {games_count} игр",
                              color=discord.Color.random())
        sorted_games = {k: v for k, v in sorted(self.game_stats.items(), key=lambda item: item[1], reverse=True)}
        for i, k in enumerate(sorted_games):
            embed.add_field(name='', value=f'{k} ({sorted_games[k]} ч.)', inline=False)
            if i == embed_maximum_fields_count - 1:
                break
        embed.set_thumbnail(url=steam_icon)
        await interaction.response.send_message(embed=embed)
