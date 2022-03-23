import time
import telegram

import requests
import logging

from requests.exceptions import ReadTimeout, HTTPError
from environs import Env

from log_handlers import TelegramChatHandler

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
BOT_TOKEN = env.str('BOT_TOKEN')
LOGS_BOT_TOKEN = env.str('LOGS_BOT_TOKEN')
CHAT_ID = env.int('CHAT_ID')

logger = logging.getLogger(__name__)


def get_long_poling_reviews(timestamp=None):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {TOKEN}'}
    response = requests.get(url, headers=headers, params={'timestamp': timestamp})
    response.raise_for_status()
    return response.json()


def notify_to_telegram(bot, data, chat_id):
    for work in data['new_attempts']:
        is_negative = work['is_negative']
        lesson_title = work['lesson_title']
        lesson_url = work['lesson_url']
        massage = f'У Вас проверили работу "{lesson_title}"\n\n'
        result = 'Преподавателю все понравилось, можно приступать к следующему уроку' if not is_negative else \
            f'К сожалению, в работе нашлись ошибки.'
        bot.send_message(text=f'{massage}{result} \n {lesson_url}', chat_id=chat_id)


def main():
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

    telegram_handler = TelegramChatHandler(token=LOGS_BOT_TOKEN, chat_id=CHAT_ID)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)

    bot = telegram.Bot(token=BOT_TOKEN)
    timestamp = None

    logger.info('Bot started')
    while True:
        try:
            reviews = get_long_poling_reviews(timestamp=timestamp)
        except ReadTimeout as e:
            logger.error(e)
            continue
        except HTTPError as e:
            logger.error(e)
            continue
        except ConnectionError:
            logger.error('Connection problems')
            time.sleep(5)
            continue
        if reviews['status'] == 'timeout':
            logger.debug('Timeout')
            timestamp = reviews['timestamp_to_request']
        if reviews['status'] == 'found':
            logger.info(reviews['new_attempts'])
            notify_to_telegram(bot, reviews, chat_id=CHAT_ID)
            timestamp = reviews['last_attempt_timestamp']


if __name__ == '__main__':
    main()
