import json
import math
from typing import List

import slack
from pydash import py_

from ccb.types import User


def load_users_from_json(json_path: str) -> List[User]:
    """
    List users from json dump of slack members.
    """

    with open(json_path) as fp:
        members = json.load(fp)

    users = []
    for member in members:
        if member["is_bot"]:
            continue
        if member["deleted"]:
            continue
        if member["id"] == "USLACKBOT":
            continue
        users.append(User(member["id"], member["real_name"]))

    return users


def list_users_from_user_group(client: slack.WebClient, user_group: str) -> List[User]:
    raise NotImplementedError()


def list_users(client: slack.WebClient) -> List[User]:
    """
    List workspace users.
    """

    response = client.users_list()
    members = response["members"]

    users = []
    for member in members:
        if member["is_bot"]:
            continue
        if member["deleted"]:
            continue
        if member["id"] == "USLACKBOT":
            continue
        users.append(User(member["id"], member["real_name"]))
    return users


def group_items(items: List, n: int) -> List[List]:
    """
    Group items in group of max size n. More larger groups are preferred
    instead of less smaller ones.
    """

    n_groups = math.ceil(len(items) / n)

    base_size = (len(items) // n_groups) + 1
    base_n_groups = len(items) % n_groups

    rest_size = base_size - 1
    rest_n_groups = n_groups - base_n_groups

    groups = []

    start = 0
    for _ in range(base_n_groups):
        end = start + base_size
        groups.append(items[start:end])
        start = end

    for _ in range(rest_n_groups):
        end = start + rest_size
        groups.append(items[start:end])
        start = end

    return groups


def channel_name_to_id(name: str, client: slack.WebClient) -> str:
    """
    Return slack id for given channel name.
    """

    response = client.users_conversations(types="public_channel,private_channel,mpim,im", exclude_archived=True)
    channels = response["channels"]

    result = py_.find(channels, lambda ch: ch["name"] == name)

    if result:
        return result["id"]
    else:
        raise ValueError(f"Channel {name} not found")
