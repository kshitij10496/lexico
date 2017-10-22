import click
from click.testing import CliRunner

from lexicon.cli import lexicon

def test_lexicon_group():
    runner = CliRunner()
    result = runner.invoke(lexicon)
    assert result.exit_code == 0

def test_lexicon_group_help():
    runner = CliRunner()
    result = runner.invoke(lexicon, '--help')
    assert result.exit_code == 0

    help_text_stubs = (lexicon.name, lexicon.help, 'Commands', 'Options')
    assert all(help_text_stub in result.output for help_text_stub in help_text_stubs)

    subcommands = lexicon.commands.keys()
    assert all(subcommand in result.output for subcommand in subcommands)
