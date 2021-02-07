"""
Coffee catchup bot

Usage:
  ccb group --output-json=<output-json> [--n=<n>] [--seed=<seed>] [--user-group=<user-group>]
  ccb post --matches-json=<matches-json> --channel-name=<channel-name> [--template-file=<template-file>]
  ccb dm-group --matches-json=<matches-json> [--template-file=<template-file>] [--topics-file=<topics-file>]

Options:
  --n=<n>                          Max number of people in each group [default: 4]
  --seed=<seed>                    Integer seed to use instead of the default
  --matches-json=<matches-json>    File with matching information
  --channel-name=<channel-name>    Name of the channel to post the matching in
  --template-file=<template-file>  Jinja2 template file for slack post.
  --users-group=<users-group>      Pick users from given user group.
  --topics-file=<topics-file>      File with list of topic-like items to be randomly peppered in DMs.
"""

import json
import os
import random
from dataclasses import asdict

import jinja2
import slack
from docopt import docopt
from tqdm import tqdm

from ccb.core import (channel_name_to_id, group_items, load_users,
                      load_users_from_user_group)
from ccb.template import TPL_DM, TPL_MATCHES
from ccb.types import User


def main():
    args = docopt(__doc__)

    client = slack.WebClient(os.environ["SLACK_BOT_USER_TOKEN"])

    if args["group"]:
        seed = args["--seed"]
        n = int(args["--n"])

        if seed:
            seed = int(seed)

        random.seed(seed)

        if args["--user-group"]:
            users = load_users_from_user_group(client, args["--user-group"])
        else:
            users = load_users(client)

        print(f":: Found {len(users)} users")

        to_skip = {uid.strip() for uid in os.environ.get("CCB_SKIP_LIST", "").split(",")}
        if "" in to_skip:
            to_skip.remove("")

        print(f":: Skipping {len(to_skip)}")
        users = [u for u in users if u.id not in to_skip]

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

        if args["--template-file"]:
            with open(args["--template-file"]) as fp:
                template = fp.read()
        else:
            template = TPL_MATCHES

        message = jinja2.Template(template).render(groups=matches["groups"])

        channel_id = channel_name_to_id(args["--channel-name"], client)
        response = client.chat_postMessage(channel=channel_id, text=message)

        reactions = ["coffee"]
        for reaction in reactions:
            client.reactions_add(
                channel=channel_id,
                name=reaction,
                timestamp=response.data["ts"]
            )

    elif args["dm-group"]:
        # Make new group DM with the people in matches and send a message for
        # scheduling the catchup.

        topics = []
        if args["--topics-file"]:
            with open(args["--topics-file"]) as fp:
                topics = fp.read().strip().splitlines()

        with open(args["--matches-json"]) as fp:
            matches = json.load(fp)

        if args["--template-file"]:
            with open(args["--template-file"]) as fp:
                template = fp.read()
        else:
            template = TPL_DM

        tpl = jinja2.Template(template)

        matches["groups"] = [[User(u["id"], u["name"]) for u in group] for group in matches["groups"]]

        for group in tqdm(matches["groups"]):
            user_ids = [u.id for u in group]
            response = client.conversations_open(users=user_ids)

            random.shuffle(topics)
            n_topics = 3
            message = tpl.render(topics=topics[:n_topics])
            client.chat_postMessage(channel=response["channel"]["id"], text=message)
