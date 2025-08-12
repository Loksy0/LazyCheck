#!/bin/bash

CONFIG_FILE="config.json"
REQUIREMENTS_FILE="requirements.txt"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Brak pliku $CONFIG_FILE"
    exit 1
fi

VIEWDNS_KEY=$(grep -oP '"viewdns\.info_api_key"\s*:\s*"\K[^"]+' "$CONFIG_FILE")
LEAKLOOKUP_KEY=$(grep -oP '"leak-lookup\.com_api_key"\s*:\s*"\K[^"]+' "$CONFIG_FILE")

if [[ -z "$VIEWDNS_KEY" || "$VIEWDNS_KEY" == "enter_here_your_api_key" ]]; then
    echo "Pole viewdns.info_api_key w $CONFIG_FILE jest niepoprawne lub puste!"
    exit 1
fi

if [[ -z "$LEAKLOOKUP_KEY" || "$LEAKLOOKUP_KEY" == "enter_here_your_api_key" ]]; then
    echo "Pole leak-lookup.com_api_key w $CONFIG_FILE jest niepoprawne lub puste!"
    exit 1
fi

if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Brak pliku: $REQUIREMENTS_FILE"
    exit 1
fi

if ! command -v nmap &> /dev/null; then
    echo "Musisz zainstalować nmap!"
    exit 1
else
    echo "nmap jest zainstalowany."
fi
