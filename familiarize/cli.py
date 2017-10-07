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

@click.command()
@click.option('--init', is_flag=True, default=False)
@click.option('--view', is_flag=True, default=False)
@click.argument('word', required=False)
def familiarize(init, view, word):
    #print('View:', view)
    #print('Word:', word)
    if word is not None:
        handle_word(word)
    elif view:
        handle_view()
    elif init:
        handle_init()

#@click.group(invoke_without_command=True)
#@click.argument('word', type=str)
#@click.pass_context
#def dictionary(ctx, word):
    #click.echo('We are now using "dictionary".')
    #click.echo('Word passed: {}'.format(word))
    #click.echo('Handling word')
    #handle_word(word)
    #click.echo('Handled word')
#
#@dictionary.command()
#@click.argument('word', type=str)
#def new(word):
    #handle_word(word)
    
def handle_word(word):
    #click.echo('Word received by new(): {}'.format(word))
    try:
        API_KEY = load_api_key()
        #print('API_KEY:', API_KEY)
    except ConfigFileError:
        click.echo('API key is missing. Kindly provide an API key by registering via:\n\n$ familiarize --init')
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
                   'In order to learn how to use the application, use:\n\n$ familiarize --help')

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
