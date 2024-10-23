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
conn = None 

def load_keywords():
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except Exception as e:
        print(f"Error when loading keywords: {e}")
        return []

def update_keywords_pattern():
    global keywords_pattern
    keywords = load_keywords()
    keywords_pattern = '|'.join(map(re.escape, keywords))

update_keywords_pattern()

async def refresh_keywords_periodically(interval=300):
    while True:
        update_keywords_pattern()
        await asyncio.sleep(interval)

@client.on(events.NewMessage())
async def handler(event):
    global keywords_pattern
    global conn

    if event.message.is_channel and event.message.reply_to:
        return

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
            channel_name = "Channel name not available"

        message_to_send = f"Message matching: {pattern_match.group(1)}\nFrom the channel '{channel_name}':\n{message_text}\n"

        try:
            conn.sendall(message_to_send.encode())
        except BrokenPipeError:
            print("The connection was closed, reconnecting...")
            reconnect_socket()

def reconnect_socket():
    global conn
    while True:
        try:
            print("Waiting for a new connection...")
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            break
        except Exception as e:
            print(f"Connection error: {e}")

async def start_bot():
    await client.start()
    print("Running bots...")
    asyncio.create_task(refresh_keywords_periodically())
    await client.run_until_disconnected()

if __name__ == '__main__':
    reconnect_socket()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
