import time
from collections import namedtuple

import telegram

import requests
import logging

from requests.exceptions import ReadTimeout, HTTPError
from environs import Env
from vk_maria import Vk

env = Env()
env.read_env()

# Devman API token
TOKEN = env.str('TOKEN')

# Telegram bot token
BOT_TOKEN = env.str('BOT_TOKEN')
# Chat_id for notifications
CHAT_ID = env.int('CHAT_ID')

# VK Community token
VK_TOKEN = env.str('VK_TOKEN')
VK_USER_ID = env.str('VK_USER_ID')

logger = logging.getLogger(__name__)


def get_long_poling_checks(timestamp=None):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {TOKEN}'}
    response = requests.get(url, headers=headers, params={'timestamp': timestamp})
    response.raise_for_status()
    return response.json()


def notify(bots, data, chat_id, user_id):
    for work in data['new_attempts']:
        is_negative = work['is_negative']
        lesson_title = work['lesson_title']
        lesson_url = work['lesson_url']
        message = '\n'.join([
            f'У Вас проверили работу "{lesson_title}"\n\n',
            'Преподавателю все понравилось, можно приступать к следующему уроку' \
                if not is_negative else \
                f'К сожалению, в работе нашлись ошибки.',
            f'{lesson_url}'
        ])

        bots.telegram.send_message(text=message, chat_id=chat_id)
        bots.vk.messages_send(user_id=user_id, message=message)


def main():
    logging.basicConfig(level=logging.INFO)
    Bots = namedtuple('Bots', ('telegram', 'vk'))

    bots = Bots(telegram=telegram.Bot(token=BOT_TOKEN), vk=Vk(access_token=VK_TOKEN))
    timestamp = None

    while True:
        try:
            response = get_long_poling_checks(timestamp=timestamp)
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
        if response['status'] == 'timeout':
            logger.debug('Timeout')
            timestamp = response['timestamp_to_request']
        if response['status'] == 'found':
            logger.info(response['new_attempts'])
            notify(bots, response, chat_id=CHAT_ID, user_id=VK_USER_ID)
            timestamp = response['last_attempt_timestamp']


if __name__ == '__main__':
    main()
