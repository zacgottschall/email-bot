#!/bin/bash

touch $EMAIL_BOT_DIR/test.txt
git pull
source $EMAIL_BOT_DIR/venv/bin/activate
pip3 install -r $EMAIL_BOT_DIR/requirements.txt
python3 $EMAIL_BOT_DIR/main.py
deactivate