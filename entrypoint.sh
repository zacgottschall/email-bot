#!/bin/bash

git pull
[ -d "./venv" ] || python3 -m venv venv
[ -d "/email-bot-files" ] || mkdir email-bot-files
source venv/bin/activate
pip3 install -r requirements.txt
[ -f "./last_check" ] || touch "./last_check"
python3 main.py
deactivate