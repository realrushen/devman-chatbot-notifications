import time
import telegram

import requests
import logging

from requests.exceptions import ReadTimeout, HTTPError
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
BOT_TOKEN = env.str('BOT_TOKEN')
CHAT_ID = env.int('CHAT_ID')

logger = logging.getLogger(__name__)


def get_checks():
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {'Authorization': f'Token {TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_long_poling_checks(timestamp=None):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {TOKEN}'}
    params = {}
    if timestamp:
        params['timestamp'] = timestamp
    response = requests.get(url, headers=headers, params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def notify_to_telegram(bot, data, chat_id):
    for work in data['new_attempts']:
        is_nagative = work['is_negative']
        lesson_title = work['lesson_title']
        lesson_url = work['lesson_url']
        massage = f'У Вас проверили работу "{lesson_title}"\n\n'
        result = 'Преподавателю все понравилось, можно приступать к следующему уроку' if not is_nagative else \
            f'К сожалению, в работе нашлись ошибки.'
        bot.send_message(text=f'{massage}{result} \n {lesson_url}', chat_id=chat_id)


def main():
    logging.basicConfig(level=logging.DEBUG)

    bot = telegram.Bot(token=BOT_TOKEN)
    timestamp = None

    while True:
        try:
            response = get_long_poling_checks(timestamp=timestamp)
        except ReadTimeout as ex:
            logger.error(ex)
            continue
        except HTTPError as ex:
            logger.error(ex)
            continue
        except ConnectionError:
            logger.error('Connection problems')
            time.sleep(5)
            continue
        if response['status'] == 'timeout':
            logger.debug('Timeout')
            timestamp = response['timestamp_to_request']
        if response['status'] == 'found':
            logger.info(response['new_attempts'])
            notify_to_telegram(bot, response, chat_id=CHAT_ID)
            timestamp = response['last_attempt_timestamp']


if __name__ == '__main__':
    main()
