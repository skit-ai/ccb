#!/usr/bin/env bash

week=$(date +%V)

if [[ $((week % 2)) -eq 0 ]];
then
    poetry run ccb group --output-json=matches.json
    poetry run ccb post --matches-json=matches.json --channel-name=all-them-bots
else
    echo "Week number $week is even. Skipping.";
fi
