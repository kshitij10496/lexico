import click

from .errors import ConfigFileError
from .utils import fetch_word_meanings, save_api_key, load_api_key, save_word, get_words

'''
Supported Commands
==================
new - Find data about a new word
list - List all the words ever looked up
register - Prompt user to provide Wordnik API key
remove - Remove a word from the lookup table

'''
@click.group()
def dictionary():
    click.echo('We are now using "dictionary".')

@dictionary.command()
@click.argument('word', type=str)
def new(word):
    try:
        API_KEY = load_api_key()
    except ConfigFileError:
        click.echo('API key is missing. Kindly provide an API key by registering via:\t dictionary register')
    else:
        data = fetch_word_meanings(word, API_KEY)
        click.echo_via_pager('Data for the word: {}'.format(data))
        word_save_status = save_word(word)
        if word_save_status:
            click.echo('{} has been added to your personal dictionary.'.format(word))
        else:
            click.echo('{} could not be added to your dictionary'.format(word))

@dictionary.command()
def list():
    words = get_words()
    click.echo_via_pager(words)

@dictionary.command()
def register():
    LINK_README = ''
    click.echo('This application is powered by the Wordnik API.' \
        ' In order to fetch information, you will need to provide an API key to this service.\n' \
        'Learn how to get your API key here: {}'.format(LINK_README))
    api_key = click.prompt('Enter your Wordnik API key').strip()

    save_status = save_api_key(api_key)
    if save_status:
        click.echo('Your API Key is : {}'.format(api_key))
    else:
        click.echo('There is some issue with saving your API key. Kindly retry.')
