from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente
load_dotenv()

# Funzione per caricare le parole chiave dal file
def load_keywords():
    try:
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except Exception as e:
        print(f"Errore nel caricamento delle parole chiave: {e}")
        return []

# Funzione per aggiungere una parola chiave al file
def add_keyword(new_keyword):
    try:
        with open('keywords.txt', 'a') as f:
            f.write(new_keyword + '\n')
        print(f"Parola chiave '{new_keyword}' aggiunta con successo.")
    except Exception as e:
        print(f"Errore nell'aggiunta della parola chiave: {e}")

# Funzione che mostra i bottoni al comando /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Mostra le parole chiave", callback_data='list_keywords')],
        [InlineKeyboardButton("Aggiungi una parola chiave", callback_data='add_keyword')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Scegli un\'azione:', reply_markup=reply_markup)

# Funzione per gestire i bottoni premuti
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Risponde alla callback

    if query.data == 'list_keywords':
        keywords = load_keywords()
        if keywords:
            await query.edit_message_text(f"Le parole chiave sono:\n" + "\n".join(keywords))
        else:
            await query.edit_message_text("Nessuna parola chiave trovata.")

    elif query.data == 'add_keyword':
        await query.edit_message_text("Invia la parola chiave che vuoi aggiungere:")
        # Aggiungi uno stato per indicare che stai aspettando una parola chiave
        context.user_data['awaiting_keyword'] = True

# Funzione per gestire l'inserimento di una nuova parola chiave
async def handle_new_keyword(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_keyword'):
        new_keyword = update.message.text.strip()
        if len(new_keyword) > 20:
            await update.message.reply_text("La parola chiave non può superare i 20 caratteri. Riprova.")
        else:
            add_keyword(new_keyword)
            await update.message.reply_text(f"Parola chiave '{new_keyword}' aggiunta con successo!")
        # Una volta aggiunta la parola chiave, rimuovi lo stato
        context.user_data['awaiting_keyword'] = False

def main():
    # Inserisci il tuo token del bot
    token = os.getenv("TOKEN")

    # Crea un'applicazione
    application = Application.builder().token(token).build()

    # Aggiungi i gestori per i comandi e i bottoni
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    # Gestore per il messaggio dell'utente quando invia la nuova parola chiave
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_keyword))

    # Avvia il bot
    application.run_polling()

if __name__ == '__main__':
    main()
