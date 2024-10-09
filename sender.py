import os
from dotenv import load_dotenv
import socket
import asyncio
from telethon import TelegramClient

load_dotenv()


api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Crea una nuova istanza di TelegramClient
client = TelegramClient('sender', api_id, api_hash)

# Funzione per inviare il messaggio al bot
async def send_to_bot(filtered_message, channel_name):
    message_to_send = f"Messaggio dal canale '{channel_name}':\n{filtered_message}\n"
    chat_id = int(os.getenv("USER_CHAT_ID"))  # Sostituisci con l'ID della chat in cui vuoi inviare il messaggio
    try:
        await client.send_message(chat_id, message_to_send)
        print(f"Messaggio inviato correttamente!")
    except Exception as e:
        print(f"Eccezione rilevata: {e}")

# Funzione per gestire la comunicazione con il socket
async def listen_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    try:
        while True:
            data = client_socket.recv(1024)  # Ricevi i dati dal server
            if not data:
                break  # Esci dal ciclo se non ci sono dati
            shared_variable = data.decode()
            print(f"Variabile ricevuta: {shared_variable}")

            # Esegui la funzione send_to_bot quando arriva un nuovo messaggio
            await send_to_bot(shared_variable, "Nome del canale")  # Puoi personalizzare il nome del canale
    finally:
        client_socket.close()

# Funzione principale per eseguire il bot
async def start_bot():
    await client.start()
    print("Bot in esecuzione...")

    # Inizia a ascoltare il socket
    await listen_socket()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
