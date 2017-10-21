import click

from .errors import ConfigFileError
from .utils import fetch_word, save_api_key, load_api_key, save_word, get_words, check_initialization, tabulate_words

'''
Supported Commands
==================
new - Find data about a new word
list - List all the words ever looked up
register - Prompt user to provide Wordnik API key
remove - Remove a word from the lookup table

'''
@click.group()
def lexicon():
    pass

@lexicon.command()
@click.argument('word')
def new(word):
    if word:
        handle_word(word)
    #TODO: raise error

@lexicon.command()
def init():
    handle_init()

@lexicon.command()
def view():
    handle_view()

    
def handle_word(word):
    #click.echo('Word received by new(): {}'.format(word))
    try:
        API_KEY = load_api_key()
        #print('API_KEY:', API_KEY)
    except ConfigFileError:
        click.echo('API key is missing. Kindly provide an API key by registering via:\n\n$ lexicon init')
    else:
        word_object = fetch_word(word)
        click.echo_via_pager(word_object.stringify())
        word_save_status = save_word(word_object)
        if word_save_status:
            click.echo('{} has been added to your personal dictionary.'.format(word))
        else:
            click.echo('{} could not be added to your dictionary'.format(word))

#@dictionary.command()
def handle_view():
    words = get_words()
    display_words = tabulate_words(words)
    click.echo_via_pager(display_words)

def handle_init():

    # TODO: Check if the folder is already created.
    is_initialized = check_initialization()

    if is_initialized:
        click.echo('Your dictionary has already been initialised.\n' \
                   'In order to learn how to use the application, use:\n\n$ lexicon --help')

    else:
        # TODO: Move the instructions for registration to README and link them here.
        click.echo('This application is powered by the Wordnik API.' \
            ' In order to fetch information, you will need to provide an API key to this service.\n')

        api_key = click.prompt('Enter your Wordnik API key').strip()

        save_status = save_api_key(api_key)
        if save_status:
            click.echo('Your API Key is : {}'.format(api_key))
        else:
            click.echo('There is some issue with saving your API key. Kindly retry.')
