#!/bin/bash

cd ~ || exit 1

# Naviga nella directory Kometa
cd MessageFilterBot || exit 1

# Attiva l'ambiente virtuale
source messagefilter/bin/activate || exit 1

# Carica le variabili dal file .env
set -a
source .env
set +a

scraper_log_file="$LOG_PATH/scraper_bot_log_$(date +%Y-%m-%d_%H-%M-%S).log"
sender_log_file="$LOG_PATH/sender_bot_log_$(date +%Y-%m-%d_%H-%M-%S).log"

# Esegui scraper.py e redirigi stdout e stderr nel log
nohup python3 ./scraper/scraper.py -r > "$scraper_log_file" 2>&1 &
echo $! > /tmp/scraper_bot.pid

# Aspetta 10 secondi
sleep 10

# Esegui sender.py e redirigi stdout e stderr nel log
nohup python3 ./sender/sender.py -r > "$sender_log_file" 2>&1 &
echo $! > /tmp/sender_bot.pid
