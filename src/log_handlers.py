import logging
import pdb

import telegram


class TelegramChatHandler(logging.Handler):
    """
    This handler sends log records to telegram chat with chat_id
    """
    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)

        self.bot.send_message(text=log_entry, chat_id=self.chat_id)
