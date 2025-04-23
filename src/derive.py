import click
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip84,
    Bip84Coins,
    Bip86,
    Bip86Coins,
    Bip44Changes,
    Bip32Slip10Secp256k1,
    P2PKHAddr,
    P2WPKHAddr,
    P2TRAddr,
    CoinsConf,
)


def derive_wallet_info(mnemonic, index=0, fmt="legacy", show_xpub=False, path=None):
    try:
        seed = Bip39SeedGenerator(mnemonic).Generate()

        # Custom derivation path overrides standard behavior
        if path:
            bip32_ctx = Bip32Slip10Secp256k1.FromSeed(seed)
            derived = bip32_ctx.DerivePath(path)
            pub_key = derived.PublicKey()

            if show_xpub:
                return pub_key.ToExtended()
            else:
                # Use appropriate address encoder based on format
                if fmt == "legacy":
                    return P2PKHAddr.EncodeKey(
                        pub_key.KeyObject(),
                        net_ver=CoinsConf.BitcoinMainNet.ParamByKey("p2pkh_net_ver"),
                    )
                elif fmt == "segwit":
                    return P2WPKHAddr.EncodeKey(
                        pub_key.KeyObject(),
                        hrp=CoinsConf.BitcoinMainNet.ParamByKey("p2wpkh_hrp"),
                    )
                elif fmt == "taproot":
                    return P2TRAddr.EncodeKey(
                        pub_key.KeyObject(),
                        hrp=CoinsConf.BitcoinMainNet.ParamByKey("p2tr_hrp"),
                    )
                else:
                    return f"❌ Unknown format: {fmt}"

        # Standard BIP paths
        if fmt == "legacy":
            wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
        elif fmt == "segwit":
            wallet = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
        elif fmt == "taproot":
            wallet = Bip86.FromSeed(seed, Bip86Coins.BITCOIN)
        else:
            return f"❌ Unknown format: {fmt}"

        account = wallet.Purpose().Coin().Account(0)

        if show_xpub:
            return account.PublicKey().ToExtended()
        else:
            addr_obj = account.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
            return addr_obj.PublicKey().ToAddress()

    except Exception as e:
        return f"❌ Error: {e}"


@click.command()
@click.option(
    "--xpub",
    is_flag=True,
    help="Print the account-level xpub instead of a single address.",
)
@click.option("--mnemonic", "-m", required=True, help="A full 12- or 24-word mnemonic.")
@click.option(
    "--index", "-i", default=0, help="Address index to derive (default is 0)."
)
@click.option(
    "--format",
    "-f",
    "fmt",
    default="legacy",
    type=click.Choice(["legacy", "segwit", "taproot"]),
    help="Address format to derive (legacy, segwit, taproot).",
)
def main(mnemonic, index, fmt, xpub):
    result = derive_wallet_info(mnemonic, index, fmt, show_xpub=xpub)
    label = "XPUB" if xpub else f"{fmt.upper()} Address [{index}]"
    click.echo(f"🔑 {label}: {result}")


if __name__ == "__main__":
    main()
