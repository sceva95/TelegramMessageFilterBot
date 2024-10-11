#!/bin/bash

# Uccidi il bot scraper
if [ -f /tmp/scraper_bot.pid ]; then
    kill $(cat /tmp/scraper_bot.pid)
    rm /tmp/scraper_bot.pid
    echo "scraper_bot terminato"
else
    echo "scraper_bot non è in esecuzione"
fi

# Uccidi il bot sender
if [ -f /tmp/sender_bot.pid ]; then
    kill $(cat /tmp/sender_bot.pid)
    rm /tmp/sender_bot.pid
    echo "sender_bot terminato"
else
    echo "sender_bot non è in esecuzione"
fi
