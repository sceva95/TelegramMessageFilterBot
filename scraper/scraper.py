import sqlite3
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
BOT_USERNAME = os.getenv("BOT_USERNAME")
USER_CHAT_ID = int(os.getenv("USER_CHAT_ID"))
client = TelegramClient('scraper', api_id, api_hash)

conn = None 

def load_keywords_from_db():
    try:
        conn = sqlite3.connect('keywords.db')
        cursor = conn.cursor()
        cursor.execute("SELECT keyword FROM keywords")
        keywords = [row[0] for row in cursor.fetchall()]
        conn.close()
        return keywords
    except Exception as e:
        print(f"Error when loading keywords from database: {e}")
        return []

def get_keywords():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM keywords')
    rows = cursor.fetchall()
    conn.close()
    return rows

async def add_keyword(word, event):
    try:
        conn = sqlite3.connect('keywords.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO keywords (keyword) VALUES (?)', (word,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.sendall(f"Error while adding keyword {word}: {e}".encode())
        print(f"Error while adding keyword {word}: {e}")
        return False
    
def delete_keyword(id):
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM keywords WHERE id = ?', (id,))
    conn.commit()
    conn.close()

@client.on(events.NewMessage())
async def handler(event):
    global conn
    
    keywords = load_keywords_from_db()
    keywords_pattern = '|'.join(map(re.escape, keywords))

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

@client.on(events.NewMessage(pattern='/list'))
async def list_command(event):
    global conn

    if event.sender_id != USER_CHAT_ID:
        conn.sendall(f"Non hai i permessi per eseguire questo comando. {event.sender_id}".encode())
        return
    
    keywords = get_keywords()
    if not keywords:
        conn.sendall("Nessuna parola trovata.".encode())
        return

    lista_numerata = "\n".join([f"{i + 1}. {row[1]}" for i, row in enumerate(keywords)])
    conn.sendall(f"Ecco la lista delle parole:\n{lista_numerata}".encode())

@client.on(events.NewMessage(pattern='/add (.+)'))
async def add_command(event):
    global conn

    if event.sender_id != USER_CHAT_ID:
        conn.sendall(f"Non hai i permessi per eseguire questo comando. {event.sender_id}".encode())
        return

    parola = event.pattern_match.group(1)
    result = await add_keyword(parola, event) 
    if result:
        conn.sendall(f"Parola '{parola}' aggiunta con successo.".encode())
    else:
        conn.sendall("Errore nell'aggiunta della parola.".encode())

@client.on(events.NewMessage(pattern='/delete (.+)'))
async def delete_command(event):

    global conn

    if event.sender_id != USER_CHAT_ID:
        conn.sendall(f"Non hai i permessi per eseguire questo comando. {event.sender_id}".encode())
        return
    try:
        id_to_delete = int(event.pattern_match.group(1))
        keywords = get_keywords()
        if 0 < id_to_delete <= len(keywords):
            parola_rimossa = keywords[id_to_delete - 1][1]  # Ottieni la parola corrispondente
            delete_keyword(keywords[id_to_delete - 1][0])  # Elimina la parola dal database
            conn.sendall(f"Parola '{parola_rimossa}' eliminata con successo.".encode())
        else:
            conn.sendall("ID non valido. Usa un ID valido dalla lista.".encode())
    except ValueError:
        conn.sendall("Per favore specifica un ID valido. Uso: /delete <id>".encode())

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
    await client.run_until_disconnected()

if __name__ == '__main__':
    reconnect_socket()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
