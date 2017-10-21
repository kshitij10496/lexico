import click

from .errors import ConfigFileError
from .utils import fetch_word, save_api_key, load_api_key, save_word, get_words, check_initialization, tabulate_words


@click.group()
def lexicon():
    '''Your personal lexicon to help you expand your English vocabulary.'''
    #TODO: Add option for debugging.
    pass

@lexicon.command()
@click.option('--word', prompt='Your word', help='The word of interest.')
def new(word):
    '''Finds the dictionary data about a word.'''
    if word:
        handle_word(word)
    #TODO: raise error
    
    try:
        API_KEY = load_api_key()
    except ConfigFileError:
        click.echo('API key is missing. Kindly provide an API key by registering via:' \
                   '\n\n$ lexicon init\n')
    else:
        word_data = fetch_word_data(word)
        click.echo_via_pager(word_data.stringify())
        word_save_status = save_word(word_object)
        if word_save_status:
            click.echo('{} has been added to your personal dictionary.'.format(word))
        else:
            click.echo('{} could not be added to your dictionary'.format(word))


@lexicon.command()
def init():
    '''Helps you get started with using "lexicon".

    Save or update your Wordnik API Key.
    '''
    is_initialized = check_initialization()

    if is_initialized:
        click.echo('lexicon has already been initialised.\n' \
                   'In order to learn how to use it, try:\n\n$ lexicon --help\n')
    else:
        # TODO: Move the instructions for registration to README and link them here.
        click.echo('In order to fetch information, this services requires you' \
                   ' to provide a Wordnik API key.\n' \
                   'Visit http://www.wordnik.com/signup to SignUp.')

        api_key = click.prompt('Enter your Wordnik API key').strip()

        save_status = save_api_key(api_key)
        if save_status:
            click.echo('Your API Key is : {}'.format(api_key))
        else:
            click.echo('There is some issue with saving your API key. Kindly retry.')

@lexicon.command()
def view():
    '''Lists all the words learnt using "lexicon".'''
    #TODO: Option for file output
    #TODO: More information/table columns
    words = get_words()
    display_words = tabulate_words(words)
    click.echo_via_pager(display_words)
