import click


from derive.brain_wallet import (
    generate_private_key,
    generate_public_key,
    generate_bitcoin_address,
)
from derive.mnemonic_phrase import derive_wallet_info


@click.group()
def cli():
    """A CLI tool for generating Bitcoin addresses."""
    pass


@cli.command()
@click.option(
    "--passphrase",
    prompt="Enter your passphrase",
    help="The passphrase for the brain wallet.",
)
def brain_wallet(passphrase: str):
    """Generate a Bitcoin address from a passphrase."""
    try:
        private_key = generate_private_key(passphrase)
        public_key = generate_public_key(private_key)
        bitcoin_address = generate_bitcoin_address(public_key)
        click.echo(f"Bitcoin Address: {bitcoin_address}")
    except Exception as e:
        click.echo(f"❌ Error generating brain wallet: {e}")


@cli.command()
@click.option(
    "--mnemonic", prompt="Enter your mnemonic", help="The mnemonic for the wallet."
)
@click.option("--index", default=0, help="Address index to derive (default is 0).")
@click.option(
    "--format",
    default="legacy",
    type=click.Choice(["legacy", "segwit", "taproot"]),
    help="Address format to derive.",
)
@click.option(
    "--xpub",
    is_flag=True,
    help="Print the account-level xpub instead of a single address.",
)
def mnemonic_phrase(mnemonic: str, index: int, format: str, xpub: bool):
    """Generate a Bitcoin address from a mnemonic."""
    try:
        result = derive_wallet_info(mnemonic, index, format, show_xpub=xpub)
        label = "XPUB" if xpub else f"{format.upper()} Address [{index}]"
        click.echo(f"🔑 {label}: {result}")
    except Exception as e:
        click.echo(f"❌ Error generating mnemonic wallet: {e}")


if __name__ == "__main__":
    cli()
