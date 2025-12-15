import asyncio
import random

import discord
from discord import Message
from discord.ext import commands

from src.bot import OgurecBot
from src.utils import get_random_formatted_emoji, get_random_sticker

MESSAGE_RANDOM_RANGE = 450
REACTION_RANDOM_RANGE = 650
MESSAGE_GUARANTEE_LIMIT = 750


class RandomMessageCog(commands.Cog):
    def __init__(self, bot: OgurecBot):
        self.bot = bot
        self.message_counter = 0

    # ---------- helpers ----------

    @staticmethod
    def _roll(*values: int, max_value: int) -> bool:
        return random.randint(1, max_value) in values

    async def _typing_with_delay(self, channel: discord.abc.Messageable):
        async with channel.typing():
            await asyncio.sleep(random.randint(2, 6))

    # ---------- actions ----------

    async def reply_to_question(self, message: Message) -> bool:
        if self.bot.user.mentioned_in(message) and message.content and message.content[-1] in {"?", "!", "."}:
            await self._typing_with_delay(message.channel)
            return True
        return False

    async def send_random_phrase(self, message: Message) -> bool:
        if self._roll(1, 2, max_value=MESSAGE_RANDOM_RANGE):
            await self._typing_with_delay(message.channel)
            return True
        return False

    async def reply_to_ping(self, message: Message) -> bool:
        if not self.bot.user.mentioned_in(message):
            return False

        if not message.guild:
            return False

        await self._typing_with_delay(message.channel)

        if random.randint(1, 4) == 1:
            await message.channel.send(
                stickers=[get_random_sticker(message.guild)],
                reference=message,
            )
        else:
            await message.channel.send(
                get_random_formatted_emoji(message.guild),
                reference=message,
            )

        return True

    async def send_random_content(
        self,
        message: Message,
        *,
        emoji: bool,
    ) -> bool:
        trigger = self._roll(1, 2, max_value=MESSAGE_RANDOM_RANGE) or self.message_counter >= MESSAGE_GUARANTEE_LIMIT

        if not trigger or self.bot.user.mentioned_in(message):
            return False

        if not message.guild:
            return False

        self.message_counter = 0
        await self._typing_with_delay(message.channel)

        if emoji:
            await message.channel.send(
                get_random_formatted_emoji(message.guild),
                reference=message,
            )
        else:
            await message.channel.send(
                stickers=[get_random_sticker(message.guild)],
                reference=message,
            )

        return True

    async def add_random_reaction(self, message: Message):
        if not message.guild or not message.guild.emojis:
            return

        value = random.randint(1, REACTION_RANDOM_RANGE)
        if 3 <= value <= 10:
            await asyncio.sleep(random.randint(1, 4))
            await message.add_reaction(random.choice(message.guild.emojis))

    # ---------- listener ----------

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        handlers = (
            self.reply_to_question,
            self.send_random_phrase,
            self.reply_to_ping,
            lambda m: self.send_random_content(m, emoji=False),
            lambda m: self.send_random_content(m, emoji=True),
        )

        for handler in handlers:
            if await handler(message):
                return

        await self.add_random_reaction(message)
        self.message_counter += 1
