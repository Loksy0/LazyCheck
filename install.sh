#!/bin/bash

CONFIG_FILE="config.json"
REQUIREMENTS_FILE="requirements.txt"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Brak pliku $CONFIG_FILE"
    exit 1
fi

API_KEY=$(grep -oP '"api_key"\s*:\s*"\K[^"]+' "$CONFIG_FILE")

if [[ -z "$API_KEY" || "$API_KEY" == "enter_here_your_api_key" ]]; then
    echo "Field api_key w $CONFIG_FILE is wrong!"
    exit 1
fi

if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "No file: $REQUIREMENTS_FILE"
    exit 1
fi

if ! command -v nmap &> /dev/null; then
    echo "You have to install nmap!"
    exit 1
else
    echo "nmap is installed."
fi