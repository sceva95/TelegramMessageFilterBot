from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
from datetime import datetime
import asyncio
import socket

load_dotenv()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
client = TelegramClient('scraper', api_id, api_hash)

keywords_pattern = None
conn = None  # Variabile globale per la connessione

def load_keywords():
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except Exception as e:
        print(f"Errore durante il caricamento delle parole chiave: {e}")
        return []

def update_keywords_pattern():
    global keywords_pattern
    keywords = load_keywords()
    keywords_pattern = '|'.join(map(re.escape, keywords))

update_keywords_pattern()

async def refresh_keywords_periodically(interval=60):
    while True:
        update_keywords_pattern()
        await asyncio.sleep(interval)

@client.on(events.NewMessage())
async def handler(event):
    global keywords_pattern
    global conn  # Dichiara conn come globale

    if keywords_pattern is None or conn is None:
        return

    sender = await event.get_sender()
    sender_username = sender.username

    if sender_username == BOT_USERNAME:
        return

    message_text = event.message.message
    pattern_match = re.search(f"(?i).*({keywords_pattern}).*", message_text)

    if pattern_match:
        if hasattr(event.message.chat, 'title'):
            channel_name = event.message.chat.title
        elif sender_username:
            channel_name = sender_username
        else:
            channel_name = "Nome canale non disponibile"

        message_to_send = f"Messaggio dal canale '{channel_name}':\n{message_text}\n"

        # Invia il messaggio al bot connesso tramite socket
        try:
            conn.sendall(message_to_send.encode())
        except BrokenPipeError:
            print("La connessione è stata chiusa, ricollegandomi...")
            reconnect_socket()

def reconnect_socket():
    global conn
    while True:
        try:
            print("In attesa di una nuova connessione...")
            conn, addr = server_socket.accept()
            print(f"Connessione da {addr}")
            break
        except Exception as e:
            print(f"Errore nella connessione: {e}")

async def start_bot():
    await client.start()
    print("Bot in esecuzione...")
    asyncio.create_task(refresh_keywords_periodically())
    await client.run_until_disconnected()

# Esegui il client
if __name__ == '__main__':
    reconnect_socket()  # Stabilisce la connessione iniziale
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
