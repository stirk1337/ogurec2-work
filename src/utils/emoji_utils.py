import random

from discord import Guild, GuildSticker


def get_random_formatted_emoji(server: Guild) -> str:
    emoji = random.choice(server.emojis)
    if emoji.name.split('_')[0] == 'a':
        return f'<a:{emoji.name}:{emoji.id}>'
    else:
        return f'<:{emoji.name}:{emoji.id}>'


def get_random_sticker(server: Guild) -> GuildSticker:
    return random.choice(server.stickers)
