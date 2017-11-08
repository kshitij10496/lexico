import sys
import click

from .errors import ConfigFileError
from .utils import fetch_word, save_api_key, load_api_key, save_word, get_words, check_initialization, tabulate_words, initialize_db, initialize_application, has_api_key, has_db


@click.group()
def lexico():
    '''Your personal glossarist to help you expand your English vocabulary.'''
    #TODO: Add option for debugging.
    pass

@lexico.command()
@click.argument('word', required=False, default=None)
def new(word):
    '''Finds the dictionary data about a word.'''
    #TODO: raise error
    if word is None:
        word = click.prompt('Enter the word', type=str)

    try:
        API_KEY = load_api_key()
    except ConfigFileError:
        click.echo('API key is missing. Kindly provide an API key by registering via:' \
                   '\n\n$ lexico init\n')
    else:
        #TODO: separate logic based on whether the word has already been seen before or not.
        word_data = fetch_word(word)
        click.echo_via_pager(word_data.stringify())
        word_save_status = save_word(word_data)
        if word_save_status:
            click.echo('{} has been added to your personal vocabulary.'.format(word))
        else:
            click.echo('{} could not be added to your personal vocabulary'.format(word))


@lexico.command()
def init():
    '''Helps you get started with using "lexico".

    Save your Wordnik API Key.
    '''

    # Step 01: Check if application folder exists.
    # Step 02: Create it if necessary.
    # Step 03: Check if API Key is already provided.
    # Step 04: If API Key is not provided, prompt for input.
    # Step 05: Check if DB_FILE exists
    # Step 06: If not, then create necessary tables.

    is_initialized = check_initialization()
    if not is_initialized:
        initialize_application()

    is_key_present = has_api_key()
    if not is_key_present:
        # TODO: Move the instructions for registration to README and link them here.
        click.echo('In order to fetch information, this services requires you' \
               ' to provide a Wordnik API key.\n' \
               'Visit http://www.wordnik.com/signup to SignUp.')

        # Step 01: Save the API Key
        api_key = click.prompt('Enter your Wordnik API key').strip()
        save_status = save_api_key(api_key)
        if save_status:
            click.echo('Your API Key has been saved successfully\n')
        else:
            click.echo('There is some issue with saving your API key. Kindly retry.')

    is_db_initialized = has_db()
    if not is_db_initialized:
        is_init = initialize_db()
        if not is_init:
            click.echo('There is some issue with initializing your dictionary. Kindly retry.')
            sys.exit(1)

    click.echo('Your personal dictionary has been initialised.\n' \
               'In order to learn how to use it, try:\n\n$ lexico --help\n')


@lexico.command()
def view():
    '''Lists all the words present in your dictionary.'''
    #TODO: Option for file output
    #TODO: More information/table columns
    words = get_words()
    display_words = tabulate_words(words)
    click.echo_via_pager(display_words)
