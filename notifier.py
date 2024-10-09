from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Carica le variabili di ambiente
load_dotenv()

# Inserisci qui le tue credenziali API
api_id = os.getenv("API_ID")  # ID API preso da my.telegram.org
api_hash = os.getenv("API_HASH")  # Hash API preso da my.telegram.org
bot_token = os.getenv("BOT_TOKEN")  # Token del bot preso da BotFather

# Crea il client Telethon e avvialo
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Evento per gestire i nuovi messaggi
@client.on(events.NewMessage)
async def echo(event):
    # Prendi il messaggio ricevuto
    message = event.message.message

    # Rispondi con lo stesso messaggio
    # await event.respond(message)

    # Stampa il messaggio nella console (opzionale)
    print(f"Ricevuto messaggio: {message}")

# Funzione principale per mantenere il bot attivo
async def main():
    print("Bot in esecuzione...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
