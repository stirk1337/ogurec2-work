import re


def remove_user_mentions(text: str):
    pattern = r'\<\@\d+\>'
    return re.sub(pattern, '', text)
