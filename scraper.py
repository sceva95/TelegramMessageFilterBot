from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

# Inserisci qui le tue credenziali API
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
TOKEN = os.getenv("TOKEN")  # Sostituisci con il tuo token del bot

# Lista di canali da cui filtrare i messaggi
channel_usernames = ['OfferteDale', 'salottotech', 'guideinformatica1', 'offerteByToms', 
                     'vereoffertetech', 'lapaginadegliscontiDEALS', 'offertedalefashion', 
                     'MTTVIDEO', 'prodigeekOfferte', 'ERRORI_DI_PREZZO_SPAZIALI']  # Sostituisci con i nomi dei tuoi canali

# Crea una nuova istanza di TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

def load_keywords():
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except Exception as e:
        print(f"Errore durante il caricamento delle parole chiave: {e}")
        return []

keywords = load_keywords()

keywords_pattern = '|'.join(map(re.escape, keywords))  # Unisci le parole con OR (|)

async def send_to_bot(filtered_message, channel_name):
    # Messaggio da inviare al bot, includendo il nome del canale e le parole chiave abbinate
    message_to_send = (
        f"Messaggio dal canale '{channel_name}': {filtered_message}\n"
    )
    chat_id = os.getenv("CHAT_ID")  # Sostituisci con l'ID della chat in cui vuoi inviare il messaggio
    try:
        await client.send_message(chat_id, message_to_send)  # Usa il client Telethon per inviare il messaggio
        print(f"Messaggio inviato correttamente!")
    except Exception as e:
        print(f"Eccezione rilevata: ${e}")


# Evento per gestire i messaggi da canali
@client.on(events.NewMessage(pattern=f"(?i).*({keywords_pattern}).*"))
async def handler(event):
    message = event.message
    channel_name = message.chat.title if hasattr(message.chat, 'title') else "Nome canale non disponibile"
    print(f"Messaggio ricevuto: Canale ${channel_name}; \nTimestamp: ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

    await send_to_bot(message.text, channel_name)

# Funzione principale per eseguire il bot
async def start_bot():
    # Avvia il client di Telethon
    await client.start()
    print("Bot in esecuzione...")
    # Mantieni il bot attivo
    await client.run_until_disconnected()

# Esegui il client
if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
