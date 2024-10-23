from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os
import sqlite3

# Carica il token da un file .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
USER_CHAT_ID = int(os.getenv("USER_CHAT_ID"))

def get_keywords():
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM keywords')
    rows = cursor.fetchall()
    conn.close()
    return rows

async def add_keyword(word, update: Update = None):
    try:
        conn = sqlite3.connect('keywords.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO keywords (keyword) VALUES (?)', (word,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        await update.message.reply_text(f"Error while adding keyword {word}: {e}")
        print(f"Error while adding keyword {word}: {e}")
        return False


def delete_keyword(id):
    conn = sqlite3.connect('keywords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM keywords WHERE id = ?', (id,))
    conn.commit()
    conn.close()

async def list_command(update: Update, context: CallbackContext):
    keywords = get_keywords()
    if not keywords:
        await update.message.reply_text("Nessuna parola trovata.")
        return

    lista_numerata = "\n".join([f"{i + 1}. {row[1]}" for i, row in enumerate(keywords)])
    await update.message.reply_text(f"Ecco la lista delle parole:\n{lista_numerata}")

async def delete_command(update: Update, context: CallbackContext):
    if update.effective_chat.id != USER_CHAT_ID:
        await update.message.reply_text("Non hai i permessi per eseguire questo comando.")
        return

    try:
        # Ottieni l'ID dall'argomento
        id_to_delete = int(context.args[0])  

        # Controlla se l'ID esiste nel database
        keywords = get_keywords()

        keyword_to_delete = keywords[int(id_to_delete) - 1]
        print(f'{keyword_to_delete[0]}')
        print(f'{keywords}')
        if keyword_to_delete:  # Controlla se l'ID è valido
            parola_rimossa = keyword_to_delete[1]  # Trova la parola corrispondente all'ID
            delete_keyword(id_to_delete)  # Elimina la parola dal database
            await update.message.reply_text(f"Parola '{parola_rimossa}' eliminata con successo.")
        else:
            await update.message.reply_text("ID non valido. Usa un ID valido dalla lista.")
    except (IndexError, ValueError):
        await update.message.reply_text("Per favore specifica un ID valido. Uso: /delete <id>")

async def add_command(update: Update, context: CallbackContext):
    if update.effective_chat.id != USER_CHAT_ID:
        await update.message.reply_text("Non hai i permessi per eseguire questo comando.")
        return

    if context.args:
        parola = ' '.join(context.args)  
        result = await add_keyword(parola, update) 
        if result:
            await update.message.reply_text(f"Parola '{parola}' aggiunta con successo.")
    else:
        await update.message.reply_text("Per favore specifica una parola da aggiungere. Uso: /add <parola>")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("list", list_command))

    application.add_handler(CommandHandler("delete", delete_command))

    application.add_handler(CommandHandler("add", add_command))

    application.run_polling()

if __name__ == '__main__':
    main()
