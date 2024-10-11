#!/bin/bash

# Uccidi il bot scraper
if [ -f /tmp/scraper_bot.pid ]; then
    kill $(cat /tmp/scraper_bot.pid)
    rm /tmp/scraper_bot.pid
    echo "scraper_bot killed"
else
    echo "scraper_bot is not running"
fi

# Uccidi il bot sender
if [ -f /tmp/sender_bot.pid ]; then
    kill $(cat /tmp/sender_bot.pid)
    rm /tmp/sender_bot.pid
    echo "sender_bot killed"
else
    echo "sender_bot is not running"
fi
