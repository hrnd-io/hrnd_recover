import click
from mnemonic import Mnemonic
from itertools import product
from tqdm import tqdm


mnemo = Mnemonic("english")
wordlist = mnemo.wordlist


def find_missing_words(partial_mnemonic, missing_indices, show_progress=True):
    words = partial_mnemonic.split()
    results = []

    slots = [wordlist for _ in missing_indices]
    total_combinations = len(wordlist) ** len(missing_indices)

    iterator = product(*slots)
    if show_progress:
        iterator = tqdm(iterator, total=total_combinations, desc="🔍 Brute-forcing")

    for combo in iterator:
        candidate = words[:]
        for idx, word in zip(missing_indices, combo):
            candidate[idx] = word
        phrase = " ".join(candidate)

        if mnemo.check(phrase):
            results.append(phrase)

    return results


@click.command()
@click.option(
    "--mnemonic", "-m", required=True, help="Mnemonic with missing words as '____'"
)
@click.option(
    "--quiet", is_flag=True, help="Suppress result printing (but keep progress bar)."
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Optional file to save recovered mnemonics.",
)
def main(mnemonic, quiet, output):
    """
    Recover valid mnemonics by auto-detecting and brute-forcing missing words.
    """
    words = mnemonic.strip().split()
    missing_indices = [i for i, w in enumerate(words) if w.strip("_?") == ""]

    if len(words) not in [12, 15, 18, 21, 24]:
        click.echo("❌ Invalid mnemonic length.")
        return

    if not missing_indices:
        click.echo("❌ No missing words detected. Use '____' for missing ones.")
        return

    click.echo(f"🔍 Detected missing word positions: {missing_indices}")
    valid_phrases = find_missing_words(mnemonic, missing_indices)

    if valid_phrases:
        if output:
            with open(output, "w") as f:
                for phrase in valid_phrases:
                    f.write(phrase + "\n")
            click.echo(f"\n💾 Saved {len(valid_phrases)} mnemonic(s) to {output}")

        if not quiet:
            click.echo(f"\n✅ Found {len(valid_phrases)} valid mnemonic(s):")
            for i, phrase in enumerate(valid_phrases, 1):
                click.echo(f"\n#{i}: {phrase}")
        elif not output:
            click.echo(f"\n✅ Found {len(valid_phrases)} valid mnemonic(s).")
    else:
        click.echo("❌ No valid mnemonics found.")


if __name__ == "__main__":
    main()
