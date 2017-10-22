import click
from click.testing import CliRunner

from glossarist.cli import glossarist

def test_glossarist_group():
    runner = CliRunner()
    result = runner.invoke(glossarist)
    assert result.exit_code == 0

def test_glossarist_group_help():
    runner = CliRunner()
    result = runner.invoke(glossarist, '--help')
    assert result.exit_code == 0

    help_text_stubs = (glossarist.name, glossarist.help, 'Commands', 'Options')
    assert all(help_text_stub in result.output for help_text_stub in help_text_stubs)

    subcommands = glossarist.commands.keys()
    assert all(subcommand in result.output for subcommand in subcommands)
