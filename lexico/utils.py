from collections import namedtuple
from dateutil.parser import parse
import os
import json
import sqlite3

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


HOME_DIR = os.path.expanduser('~') # User's Home Directory
# Base Directory to store all data related to the application.
BASE_DIR = os.path.join(HOME_DIR, '.lexico')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
WORDS_FILE = os.path.join(BASE_DIR, 'words.json')
DB_FILE = os.path.join(BASE_DIR, 'vocabulary.db')
connection = sqlite3.connect(DB_FILE)

def save_api_key(api_key):
    '''Saves or updates the Wordnik API key in the configuration file.'''

    is_initialized = check_initialization()
    if not is_initialized:
        os.mkdir(BASE_DIR)

    if not os.path.isfile(CONFIG_FILE):
        data = {'API_KEY': api_key}
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
    '''Return the Wordnik API key saved in the configuration file.

    Raises ConfigFileError exception if the file does not exists.
    '''

    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
        api_key = data['API_KEY']
        return api_key
    else:
        raise ConfigFileError('The configuration file does not exists.')

def fetch_word(word):
    from .word import Word

    if os.path.isfile(WORDS_FILE):
        with open(WORDS_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
            
        for datapoint in data:
            if word in datapoint:
                word_data = lookup_word(word)
                if word_data is not None:
                    return Word(**word_data)
                break

        
    word_data = {'word': word}
    return Word(**word_data)

def lookup_word(word):
    if not os.path.isfile(DB_FILE):
        return None
    else:
        with open(DB_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)

        for d in data:
            word_data = json.loads(d)
            if word_data['word'] == word:
                return word_data


def save_word(word_object):
    # Save the word data to the database
    encoded_data = [word_object.jsonify()]
    if not os.path.isfile(DB_FILE):
        with open(DB_FILE, 'w') as file:
            file.write(json.dumps(encoded_data))
    else:
        with open(DB_FILE, 'r') as file:
            data = file.read()

        json_data = json.loads(data)
        json_data.extend(encoded_data)

        encoded_data = json.dumps(json_data)
        with open(DB_FILE, 'w') as file:
            file.write(encoded_data)

    # Add word to lookup table
    word = word_object.word
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
    '''Fetches list of all the words the user has looked up.'''

    if not os.path.isfile(WORDS_FILE):
        return 'No words are currently present in your glossarist.'
    else:
        with open(WORDS_FILE, 'r') as file:
            encoded_data = file.read()

        data = json.loads(encoded_data)
        formatted_data = [(word_data[0], arrow.Arrow.fromdatetime(parse(word_data[1])).humanize()) for word_data in data]

        return formatted_data

def tabulate_words(formatted_data):
    '''Tabulates the given words for user viewing.'''

    return tabulate(formatted_data, headers=['Word', 'Created'])

def check_initialization():
    '''Checks whether the application has been initilialized for the user or not.

    Returns True if the application folder, along with the configuration file exists.
    '''

    return os.path.exists(BASE_DIR)

def initialize_application():
    os.mkdir(BASE_DIR)

def has_api_key():
    try:
        _ = load_api_key()
    except ConfigFileError:
        return False
    else:
        return True

def has_db():
    # Check if the tables exist in the database with the required schemas.
    return os.path.exists(DB_FILE)

def initialize_db():
    '''Initializes the user's vocabulary by creating necessary tables.

    Returns False if the initialization fails else return True.
    '''
    with sqlite3.connect(DB_FILE) as connection:
        with connection.cursor() as cursor:
            # Step 1: Create Words Table
            cursor.execute('''CREATE TABLE Words (
                                            id                  INTEGER NOT NULL,
                                            word                TEXT NOT NULL,
                                            lookup              INTEGER,
                                            created_at          TEXT,
                                            last_lookup_at      TEXT,
                                            num_meanings        INTEGER,
                                            num_synonyms        INTEGER,
                                            num_antonyms        INTEGER,
                                            num_phrases         INTEGER,
                                            num_examples        INTEGER,
                                            num_pronunciations  INTEGER,
                                            num_hyphenations    INTEGER,
                                            PRIMARY KEY(id)
                                        )''')
            # Step 2: Create related tables
            tables = ('Meanings', 'Synonyms', 'Antonyms', 'Examples', 'Phrases',
                      'Pronunciations', 'Hyphenations')
            create_table_query = '''CREATE TABLE (?) (
                                                id      INTEGER NOT NULL,
                                                text    TEXT,
                                                word_id INTEGER NOT NULL,
                                                PRIMARY KEY(id),
                                                FOREIGN KEY(word_id) REFERENCES Word(id)
                                            )'''
            cursor.executemany(create_table_query, tables)
    
    return True
    