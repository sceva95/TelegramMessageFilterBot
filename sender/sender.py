import os
from dotenv import load_dotenv
import socket
import asyncio
from telethon import TelegramClient
from datetime import datetime

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient('sender', api_id, api_hash)

async def send_to_bot(message_to_send):
    chat_id = int(os.getenv("USER_CHAT_ID"))
    try:
        await client.send_message(chat_id, message_to_send)
        print(f"Messaggio inviato correttamente!")
    except Exception as e:
        print(f"Eccezione rilevata: {e}")

async def listen_socket():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 12345))

            current_time = datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

            await send_to_bot(f'Sender bot connesso!\nTimestamp: {timestamp}')

            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print("Connessione chiusa dal server.")
                        break
                    shared_variable = data.decode()
                    print(f"Variabile ricevuta: {shared_variable}")
                    await send_to_bot(shared_variable)

            finally:
                current_time = datetime.now()
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                client_socket.close()
                await send_to_bot(f'Connessione chiusa!\nTimestamp: {timestamp}\nTentativo di riconnessione...')
                print("Connessione chiusa, tentativo di riconnessione...")
        
        except (ConnectionRefusedError, socket.error) as e:
            print(f"Errore di connessione: {e}. Riprovo tra 5 secondi...")
            await asyncio.sleep(5)

        except Exception as e:
            print(f"Errore inatteso: {e}.")
            await asyncio.sleep(5)

async def start_bot():
    await client.start()
    print("Bot in esecuzione...")

    await listen_socket()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
