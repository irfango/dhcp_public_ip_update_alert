import requests
import json
import configparser as cfg

class telegram_chatbot():

    def __init__(self, telegram_config):
        self.telegram_bot_token = self.read_token_from_config_file(telegram_config)
        self.base = "https://api.telegram.org/bot{}".format(self.telegram_bot_token)

    # Get updates
    def get_updates(self, offset=None):
        url = self.base + '/getUpdates?timeout=100'
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content.decode('utf-8'))
    
    # Sending a message
    def send_message(self, msg, chat_id):
        url = self.base + "/sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    # Get configuration information
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'telegram_bot_token')

