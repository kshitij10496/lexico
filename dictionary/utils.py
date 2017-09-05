import os
import json

from wordnik import *

from .errors import ConfigFileError

API_URL = 'http://api.wordnik.com/v4'
#apiKey = 'eb7b4a1de6eb7f786f00e0855d106b494410425f9b1e6fa14'

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
