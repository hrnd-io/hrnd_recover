import click
from hrnd.recover import recover
from hrnd.derive import cli as derive_cli


@click.group()
def cli():
    """HRND — Hardened Bitcoin Key Recovery CLI"""
    pass


# Add flat subcommands
cli.add_command(recover)

# Add grouped commands from derive/
cli.add_command(derive_cli, name="derive")
