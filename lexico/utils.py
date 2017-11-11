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

###############################################################################
############################ INITIALIZATION ###################################
###############################################################################

def check_initialization():
    '''Checks whether the application has been initilialized for the user or not.

    Returns True if the application folder exists.
    '''
    return os.path.exists(BASE_DIR)

def initialize_application(check=True):
    '''Creates a new application directory.

    Parameters
    ----------
    check: boolean (default: True)
        Check whether the application has been initilialized before.

    NOTE: This function can be used to permanently clean the application directory.

    '''
    if check:
        if check_initialization():
            return

    os.mkdir(BASE_DIR)

def has_api_key():
    '''Checks if the Wordnik API key has been provided by the user or not.'''
    try:
        _ = load_api_key()
    except ConfigFileError:
        return False
    else:
        return True

def has_db():
    '''Checks if the vocabulary database has been created or not.'''
    # TODO: Check if the database has the desired schema.
    return os.path.exists(DB_FILE)

def initialize_db():
    '''Initializes the user's vocabulary by creating the necessary table.

    Returns False if the initialization fails else return True.
    '''
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        # Step 1: Create Words Table
        create_words_table = '''CREATE TABLE Words (
                                        id                  INTEGER NOT NULL,
                                        word                TEXT NOT NULL,
                                        lookup              INTEGER,
                                        created_at          TEXT,
                                        last_lookup_at      TEXT,
                                        PRIMARY KEY(id)
                                    )'''
        cursor.execute(create_words_table)

        # Step 2: Create Vocabulary tables
        # The "type" field of the table can have a value among:
        #   - 'Meaning'
        #   - 'Synonym'
        #   - 'Antonym'
        #   - 'Example'
        #   - 'Phrase'
        #   - 'Pronunciation'
        #   - 'Hyphenation'

        create_vocabulary_table = '''CREATE TABLE Vocabulary (
                                            id INTEGER PRIMARY KEY,
                                            type TEXT,
                                            text TEXT,
                                            word_id INTEGER NOT NULL,
                                            FOREIGN KEY(word_id) REFERENCES Word(id)
                                        )'''

        cursor.execute(create_vocabulary_table)
        connection.commit()

    return True

def save_api_key(api_key):
    '''Saves or updates the Wordnik API key in the configuration file.'''
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

    if not has_db():
        raise ConfigFileError()
    else:
        is_present, word_object = lookup_word(word)
        if not is_present:
            # Make API call
            API_KEY = load_api_key()
            word_api = create_word_api(API_KEY)
            word_object = Word(word)

            # Store result in the Words and Vocabulary table
            save_word(word_object)
            
        return word_object


def lookup_word(word):

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        search_word_query = '''SELECT * FROM Words WHERE word = (?)'''
        vocab_query = '''SELECT * FROM Vocabulary JOIN Words
                         ON Vocabulary.word_id = Words.id
                         AND Words.word = (?)'''
        
        for result in cursor.execute(search_word_query, [word]):
            word_db = WordDB(*result)


        

def save_word(word_object):
    pass
    
def get_words():
    search_word_query = '''SELECT word, lookup, created_at, last_lookup_at FROM Words'''

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute(search_word_query)
        words = cursor.fetchall()

    return words

def format_words(words):

    return [(word, lookup, arrow.get(created_at).humanize(), arrow.get(last_lookup_at).humanize())
            for word, lookup, created_at, last_lookup_at in words]
        
def tabulate_words(formatted_data):
    '''Tabulates the given words for user viewing.'''

    return tabulate(formatted_data, headers=['Word', 'Lookups', 'Created At', 'Last Lookup'])

