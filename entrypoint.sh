#!/bin/bash

touch /home/zacharygottschall/email-bot/test.txt
/usr/bin/git pull
source /home/zacharygottschall/email-bot/venv/bin/activate
/home/zacharygottschall/email-bot/venv/bin/pip3 install -r /home/zacharygottschall/email-bot/requirements.txt
/home/zacharygottschall/email-bot/venv/bin/python3 /home/zacharygottschall/email-bot/main.py
touch /home/zacharygottschall/email-bot/test2.txt
deactivate