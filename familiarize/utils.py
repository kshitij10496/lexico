from collections import namedtuple
from dateutil.parser import parse
import os
import json

import arrow
from wordnik import *
from tabulate import tabulate

from .errors import ConfigFileError

API_URL = 'http://api.wordnik.com/v4'

WordData = namedtuple('WordData', ['word', 'created_at'])

def create_word_api(API_KEY):
    client = swagger.ApiClient(API_KEY, API_URL)
    wordApi = WordApi.WordApi(client)
    return wordApi

def fetch_word(word):
    from .word import Word

    return Word(word)
    

HOME_DIR = os.path.expanduser('~') # User's Home Directory
 # Base Directory to store all data related to Dictionary App
BASE_DIR = os.path.join(HOME_DIR, '.dictionary')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
WORDS_FILE = os.path.join(BASE_DIR, 'words.json')

def save_api_key(api_key):
    is_initialized = check_initialization()
    if not is_initialized:
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
    word_data = WordData(word, arrow.now().for_json())

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
        formatted_data = [(word_data[0], arrow.Arrow.fromdatetime(parse(word_data[1])).humanize()) for word_data in data]

        return formatted_data

def tabulate_words(formatted_data):
        return tabulate(formatted_data, headers=['Word', 'Created'])

def check_initialization():
    '''Checks whether the application has been initilialized for the user or not.

    Returns True if the application folder exists, else False.

    '''
    if os.path.exists(BASE_DIR):
        return True

    return False
