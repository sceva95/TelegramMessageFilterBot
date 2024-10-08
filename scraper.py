from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os

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

# Funzione per filtrare i messaggi
async def filter_notifications(message):
    keywords = load_keywords() # Parole chiave da filtrare
    message_text = message.text.lower()
    channel_name = message.chat.title if hasattr(message.chat, 'title') else "Nome canale non disponibile"
    # Se il messaggio contiene una delle parole chiave
    matched_keywords = [keyword for keyword in keywords if keyword.lower() in message_text]
    
    # Se ci sono parole chiave corrispondenti
    if matched_keywords:
        matched_keywords_str = ', '.join(matched_keywords)  # Unisci le parole chiave abbinate in una stringa
        print(f"Notifica importante trovata nel canale '{message.peer_id}': {message.text}, matcha {matched_keywords_str}")
        # Invia il messaggio filtrato al bot includendo le parole chiave abbinate
        await send_to_bot(message.text, channel_name, matched_keywords_str)

async def send_to_bot(filtered_message, channel_name, matched_keywords):
    # Messaggio da inviare al bot, includendo il nome del canale e le parole chiave abbinate
    message_to_send = (
        f"Messaggio dal canale '{channel_name}': {filtered_message}\n"
        f"Parole chiave abbinate: {matched_keywords}"
    )
    chat_id = os.getenv("CHAT_ID")  # Sostituisci con l'ID della chat in cui vuoi inviare il messaggio
    await client.send_message(chat_id, message_to_send)  # Usa il client Telethon per inviare il messaggio

# Evento per gestire i messaggi da canali
@client.on(events.NewMessage(chats=channel_usernames))
async def handler(event):
    message = event.message
    await filter_notifications(message)

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
