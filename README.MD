# Telegram Message Filter Bot

This program is for starting a Telegram bot that filters notifications based on keywords entered in the database.

## Steps to Start

1. Create a Telegram bot. [See instructions here](#creating-a-telegram-bot).
2. Create a connection for **Telethon API**. [See instructions below](#configuring-the-env-file).
3. Create a new virtual environment and install requirements. [See instructions below](#setup).
4. Execute `scraper.py` and use your telephone number (with country code) to look at the notifications. [See instructions below](#first-startup-of-scraperpy).
5. Execute `sender.py` and use the token of your already created Telegram bot. [See instructions below](#first-startup-of-senderpy).
6. Execute `editor.py` and use the token of your already created Telegram bot. [See instructions below](#first-startup-of-editorpy).

## Guide to Creating a Telegram Bot

This guide will show you how to create a Telegram bot, configure it, and run it using a shell script.

### Prerequisites

- A Telegram account

### Creating a Telegram Bot

1. **Open Telegram** and search for the bot [@BotFather](https://t.me/botfather).
2. Start a chat with BotFather and use the command `/newbot` to create a new bot.
3. Follow the instructions to give your bot a name and a username.
4. Once created, BotFather will provide you with an **access token**. Save this token as you will use it to authenticate your bot.

### Configuring the `.env` File

Rename `.env.template` to `.env` and populate it with the following variables:


#### Obtaining Variables for the `.env` File

- **TOKEN**: This is the token you received from BotFather when you created your bot. It typically looks like `0123456789:abcd...`.
  
- **API_HASH**: You can obtain this by creating a new application on the [Telegram My Apps page](https://my.telegram.org/apps). After logging in, click on "API development tools," and you will find your API_HASH.

- **API_ID**: This is also obtained from the Telegram My Apps page when you create a new application. It will be listed alongside your API_HASH.

- **CHAT_ID**: This is the username of your Telegram bot, prefixed with `@`. For example, if your bot's username is `MyBot`, then the CHAT_ID would be `@MyBot`.

- **BOT_USERNAME**: This is the username of your bot (the one you set when creating it with BotFather) without the `@` symbol. For example, if your bot's username is `MyBot`, you should enter `MyBot`.

- **USER_CHAT_ID**: This is the chat ID of the user or group you want to send messages to. You can obtain your user chat ID by starting a chat with @userinfobot.

- **LOG_PATH**: This is the path to the folder where you want to store log files. You can set it to a relative or absolute path based on your project structure.

### Setup

1. **Create a new virtual environment**:

   ```bash
   python -m venv messagefilter

2. **Activate the virtual environment**:
   
   windows
   ```
   messagefilter\Scripts\activate
   ```

   linux
   ```bash
   source messagefilter/bin/activate

3. **Install the required packages**:
  
   Make sure you have a requirements.txt file in the root of your project. You can install the required packages using:

   ``` 
   pip install -r requirements.txt

### First startup of scraper.py

At first start of the bot he will ask 

`Please enter your phone (or bot token):`

here you have to insert your **PHONE NUMBER**

**On telegram you will see a notification with a code, insert it on the terminal and accept the connection.**

### First startup of sender.py

At first start of the bot he will ask 

`Please enter your phone (or bot token):`

here you have to insert your **TELEGRAM BOT TOKEN**


When both sender and scraper are up and running they open a socket connection on 

**localhost:12345**

You can edit it with the liked port on both scraper.py and sender.py

***Perform the above steps to start the two bots in a virtual environment and connect them to telegram***

### First startup of editor.py

This script allow telegram bot to accept 3 commands:

1. `/list`: Return the list id - value of the keywords
2. `/add word`: Accept a word to be added on the db
3. `/delete id`: Accept an id and delete that word

## starter.sh and kill_bot.sh

Inside `scripts` folder there's two .sh file

### The first one: starter.sh

It pulls from the repo, open a virtual env named `messagefilter` and starts the two bots by saving the pids to a temp file

### The second one: kill_bot.sh

It read the two pids from temp file and kill them

## Conclusion

You have now configured the necessary files to start your Message Filter Bot! 

Make sure to follow the steps carefully and fill out the `.env` file correctly.
