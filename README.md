# Notifications for devman.org

This is simple telegram bot that uses dvmn.org REST API long polling endpoint to get new code reviews and send private
messages to you.

### How to install

_Important note:_ To run this bot you need **python 3.9** already installed.

1. Clone repository `git clone https://github.com/realrushen/devman-chatbot-notifications.git`
2. Init virtual environment `python3 -m venv venv`
3. Activate virtual environment `source ./venv/bin/activate`
4. Install dependencies `pip3 install -r requirements.txt`
5. Create .env file `cd ./src && touch .env`
6. Specify `TOKEN` - dvmn.org API token that you can get [here](https://dvmn.org/api/docs/),
   `BOT_TOKEN` - telegram bot token from [botfather](https://t.me/botfather),
   `CHAT_ID` - your telegram _chat_id_,
   `LOGS_BOT_TOKEN` - telegram bot token for bot that sends logs

Now all ready to start bot with `python3 ./main.py`

### Deploy using Heroku Git

#### Install the Heroku CLI

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line).

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```bash
$ heroku login
```

#### Clone the repository

Use Git to clone source code to your local machine.

```bash
$ git clone https://github.com/realrushen/devman-chatbot-notifications.git
$ cd devman-chatbot-notifications
```

#### Setting up heroku webapp

Create your new webapp and add Evironment Variables from _How to install_ section to Config Vars in Heroku webapp settings.

#### Add remote Heroku repository and push code to it

```bash
$ heroku git:remote -a your_app_name
$ git push heroku main
```
It will install the required libraries in the requirements.txt file using pip.
Then, it will read the Procfile which specifies that the main.py file is to be executed.

#### Start worker to run main.py script that sends notifications
```bash
$ heroku ps:scale worker=1
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).