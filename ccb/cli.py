"""
Coffee catchup bot

Usage:
  ccb group --output-json=<output-json> [--n=<n>] [--seed=<seed>]
  ccb post --group-json=<group-json> --channel-name=<channel-name>

Options:
  --n=<n>                          Max number of people in each group [default: 4]
  --seed=<seed>                    Integer seed to use instead of the default
  --group-json=<group-json>        File with matching information
  --channel-name=<channel-name>    Name of the channel to post the matching in
"""

import json
import os
import random
from dataclasses import asdict

from docopt import docopt

import slack
from ccb.core import group_items, list_users


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
        random.shuffle(users)
        groups = group_items(users, n)

        output = {
            "groups": [[asdict(u) for u in group] for group in groups],
            "seed": seed
        }

        with open(args["--output-json"], "w") as fp:
            json.dump(output, fp, indent=2)

    elif args["post"]:
        raise NotImplementedError("Posting not implemented yet.")
