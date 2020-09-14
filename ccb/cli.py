"""
Coffee catchup bot

Usage:
  ccb group --output-json=<output-json> [--n=<n>] [--seed=<seed>]
  ccb post --matches-json=<matches-json> --channel-name=<channel-name>

Options:
  --n=<n>                          Max number of people in each group [default: 4]
  --seed=<seed>                    Integer seed to use instead of the default
  --matches-json=<matches-json>    File with matching information
  --channel-name=<channel-name>    Name of the channel to post the matching in
"""

import json
import os
import random
from dataclasses import asdict
from typing import List

from docopt import docopt

import slack
from ccb.core import channel_name_to_id, group_items, list_users
from ccb.types import User


def format_group(group: List[User]) -> str:
    return " ".join([f"<@{u.id}>" for u in group])


def format_matches(matches) -> str:
    lines = ["Here are the coffee matches!"]
    lines.append("\n")
    for i, group in enumerate(matches["groups"]):
        lines.append(f"group {i + 1}: " + format_group(group))

    lines.append("\n")
    lines.append(f"Seed: {matches['seed']}")
    return "\n".join(lines)


def main():
    args = docopt(__doc__)

    client = slack.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])

    if args["group"]:
        seed = args["--seed"]
        n = int(args["--n"])

        if seed:
            seed = int(seed)

        random.seed(seed)
        users = list_users(client)

        print(f":: Found {len(users)} users")
        print(f":: Making groups of max size {n}")

        random.shuffle(users)
        groups = group_items(users, n)

        output = {
            "groups": [[asdict(u) for u in group] for group in groups],
            "seed": seed
        }

        with open(args["--output-json"], "w") as fp:
            json.dump(output, fp, indent=2)

    elif args["post"]:
        with open(args["--matches-json"]) as fp:
            matches = json.load(fp)

        matches["groups"] = [[User(u["id"], u["name"]) for u in group] for group in matches["groups"]]
        message = format_matches(matches)

        channel_id = channel_name_to_id(args["--channel-name"], client)
        response = client.chat_postMessage(channel=channel_id, text=message)

        reactions = ["coffee"]
        for reaction in reactions:
            client.reactions_add(
                channel=channel_id,
                name=reaction,
                timestamp=response.data["ts"]
            )
