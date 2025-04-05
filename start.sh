#!/bin/bash

# Start Flask server in background
python3 server.py &

# Start Telegram Bot
python3 bot.py
