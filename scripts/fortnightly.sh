#!/usr/bin/env bash

week=$(date +%V)

if [[ $((week % 2)) -eq 0 ]];
then
    echo "Week number $week is even. Skipping.";
else
    poetry run ccb group --output-json=matches.json
    poetry run ccb post --matches-json=matches.json --channel-name=random --template-file=./assets/vai.j2
fi
