# Notifications for devman.org

This is simple telegram bot that uses dvmn.org REST API long polling endpoint to get new code reviews and send private
messages to you.

### How to install

_Important note:_ To run this bot you need **python 3.9** already installed.

1. Clone repository `git clone https://github.com/realrushen/devman-chatbot-notifications.git`
2. Init virtual environment `python3 -m venv venv`
3. Activate virtual environment `source ./venv/bin/activate`
4. Install dependencies `pip install -r requirements.txt`
5. Create .env file `cd ./src && touch .env`
6. Specify `TOKEN` - dvmn.org API token that you can get [here](https://dvmn.org/api/docs/),
   `BOT_TOKEN` - telegram bot token from [botfather](https://t.me/botfather) and
   `CHAT_ID` - your telegram _chat_id_

Now all ready to start bot with `python3 ./main.py`

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).