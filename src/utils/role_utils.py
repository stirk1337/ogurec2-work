from typing import List

from discord import Guild, Member, Role


def get_all_users_with_role(server: Guild, role_name: str) -> List[Member]:
    role_id = server.roles[0]
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    users = []
    for member in server.members:
        if role_id in member.roles:
            users.append(member)
    return users


def get_role_by_name(server: Guild, role_name: str) -> Role | None:
    for role in server.roles:
        if role_name == role.name:
            return role
