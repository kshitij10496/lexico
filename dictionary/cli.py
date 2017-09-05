import click

@click.group()
def dictionary():
    click.echo('We are now using "dictionary".')

@dictionary.command('')
@click.argument('word', type=str)
def new(word):
    click.echo('The meaning of the word: {}'.format(word))

@dictionary.command()
def list():
    click.echo_via_pager('List of words')
