from datetime import datetime
import os
import json

from wordnik import *
from tabulate import tabulate

from .errors import ConfigFileError

API_URL = 'http://api.wordnik.com/v4'

def fetch_word_meanings(word, API_KEY):
    client = swagger.ApiClient(API_KEY, API_URL)
    wordApi = WordApi.WordApi(client)
    definitions = wordApi.getDefinitions(word, limit=5)
    data = [definition.text for definition in definitions]
    return data


HOME_DIR = os.path.expanduser('~') # User's Home Directory
 # Base Directory to store all data related to Dictionary App
BASE_DIR = os.path.join(HOME_DIR, '.dictionary')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
WORDS_FILE = os.path.join(BASE_DIR, 'words.json')

def save_api_key(api_key):
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)

    if not os.path.isfile(CONFIG_FILE):
        data = {'API_KEY': api_key}
        encoded_data = json.dumps(data) # Encoding the data to JSON

        with open(CONFIG_FILE, 'w') as file:
            file.write(encoded_data) # Writing data to the Configuration file
    else:
        with open(CONFIG_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data) # Decoding stored JSON to a Python dict
        # TODO: Prompt the user if an old API key exists
        data['API_KEY'] = api_key
        encoded_data = json.dumps(data) # Encoding the data to JSON

        # Write data to the Config file
        with open(CONFIG_FILE, 'w') as file:
            file.write(encoded_data) # Writing data to the Configuration file

    return True


def load_api_key():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
        api_key = data['API_KEY']
        return api_key
    else:
        raise ConfigFileError('The configuration file does not exists.')

def save_word(word):
    word_data = {
                    'word': word,
                    'created_at': str(datetime.utcnow())
                }

    if not os.path.isfile(WORDS_FILE):
        data = [word_data]
        encoded_data = json.dumps(data)

        with open(WORDS_FILE, 'w') as file:
            file.write(encoded_data)
    else:
        with open(WORDS_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
        data.append(word_data)
        # TODO: Do not add word if it is already present in my vocabulary.
        encoded_data = json.dumps(data)

        with open(WORDS_FILE, 'w') as file:
            file.write(encoded_data)

    return True

def get_words():

    if not os.path.isfile(WORDS_FILE):
        return 'No words added to your dictionary yet.'
    else:
        with open(WORDS_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
        return tabulate(data, headers='keys')
