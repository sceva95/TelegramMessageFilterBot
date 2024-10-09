from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
from datetime import datetime
import asyncio
import socket
import time

load_dotenv()

# Crea un socket per il server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
# Inserisci qui le tue credenziali API
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
TOKEN = os.getenv("TOKEN")  # Sostituisci con il tuo token del bot

# Crea una nuova istanza di TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

print("In attesa di connessioni...")
conn, addr = server_socket.accept()
print(f"Connessione da {addr}")

# Variabile globale per il pattern dinamico
keywords_pattern = None

# Funzione per caricare le parole chiave
def load_keywords():
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except Exception as e:
        print(f"Errore durante il caricamento delle parole chiave: {e}")
        return []

# Funzione per aggiornare il pattern dinamico
def update_keywords_pattern():
    global keywords_pattern
    keywords = load_keywords()
    keywords_pattern = '|'.join(map(re.escape, keywords))  # Unisci le parole chiave con OR (|)

# Aggiorna il pattern per la prima volta
update_keywords_pattern()

# Coroutine che aggiorna il pattern a intervalli regolari
async def refresh_keywords_periodically(interval=30):
    while True:
        update_keywords_pattern()
        print(f"Pattern aggiornato: {keywords_pattern}")
        await asyncio.sleep(interval)  # Attendi l'intervallo prima di ricaricare

# Evento per gestire i messaggi da canali con il pattern aggiornato
@client.on(events.NewMessage())
async def handler(event):
    global keywords_pattern

    if keywords_pattern is None:
        return

    # Verifica se il messaggio contiene almeno una delle parole chiave
    message_text = event.message.message

    pattern_match = re.search(f"(?i).*({keywords_pattern}).*", message_text)

    if pattern_match:
        channel_name = event.message.chat.title if hasattr(event.message.chat, 'title') else "Nome canale non disponibile"
        print(f"Messaggio ricevuto: Canale {channel_name}; Match: ${pattern_match} \nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
        # Invia il messaggio filtrato al bot
        # await send_to_bot(message_text, channel_name)
        conn.sendall(message_text.encode())

# Funzione principale per eseguire il bot
async def start_bot():
    # Avvia il client di Telethon
    await client.start()
    print("Bot in esecuzione...")
    # Avvia il task per aggiornare le parole chiave periodicamente
    asyncio.create_task(refresh_keywords_periodically())
    # Mantieni il bot attivo
    await client.run_until_disconnected()

# Esegui il client
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
