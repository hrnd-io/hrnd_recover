import click
from mnemonic import Mnemonic
from itertools import product
from tqdm import tqdm
from rapidfuzz import fuzz, process


mnemo = Mnemonic("english")
wordlist = mnemo.wordlist

# Define the global variable
quiet_option = False


def conditional_echo(message: str) -> None:
    if not quiet_option:
        click.echo(message)


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


def correct_typos(mnemonic: str, wordlist: list[str]) -> str:
    words = mnemonic.split()
    corrected_words = []
    for word in words:
        if word not in wordlist:
            # Find the closest match in the wordlist
            closest_match = process.extractOne(word, wordlist, scorer=fuzz.ratio)
            if closest_match:
                conditional_echo(
                    f"🔍 Checking '{word}' against wordlist, closest match: '{closest_match[0]}' with score {closest_match[1]}"
                )
            if (
                closest_match and closest_match[1] > 70
            ):  # Lowered threshold for similarity
                corrected_words.append(closest_match[0])
                conditional_echo(f"✅ Corrected '{word}' to '{closest_match[0]}'")
            else:
                corrected_words.append(word)
                conditional_echo(f"❌ No suitable correction for '{word}'")
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)


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
    global quiet_option
    quiet_option = quiet
    # Skip correction for placeholders
    if "_" in mnemonic or "?" in mnemonic:
        words = mnemonic.strip().split()
        missing_indices = [i for i, w in enumerate(words) if w.strip("_?") == ""]

        if len(words) not in [12, 15, 18, 21, 24]:
            click.echo("❌ Invalid mnemonic length.")
            return

        if not missing_indices:
            click.echo("❌ No missing words detected. Use '____' for missing ones.")
            return

        conditional_echo(f"🔍 Detected missing word positions: {missing_indices}")

        valid_phrases = find_missing_words(mnemonic, missing_indices)

        if valid_phrases:
            if output:
                with open(output, "w") as f:
                    for phrase in valid_phrases:
                        f.write(phrase + "\n")
                conditional_echo(
                    f"\n💾 Saved {len(valid_phrases)} mnemonic(s) to {output}"
                )
            conditional_echo(f"\n✅ Found {len(valid_phrases)} valid mnemonic(s):")
            for i, phrase in enumerate(valid_phrases, 1):
                conditional_echo(f"\n#{i}: {phrase}")
        else:
            conditional_echo("❌ No valid mnemonics found.")
        return

    # Correct typos in the mnemonic
    corrected_mnemonic = correct_typos(mnemonic, wordlist)
    if corrected_mnemonic != mnemonic:
        conditional_echo(f"🔍 Corrected mnemonic: {corrected_mnemonic}")
    mnemonic = corrected_mnemonic

    # Validate the mnemonic
    if not mnemo.check(mnemonic):
        conditional_echo("❌ Invalid mnemonic after correction.")
        return

    conditional_echo("✅ Mnemonic is complete and valid.")


if __name__ == "__main__":
    main()
