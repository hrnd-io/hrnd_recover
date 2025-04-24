import pytest
from hrnd.recover import find_missing_words
from click.testing import CliRunner
from hrnd.recover import cli


def test_find_missing_words():
    partial_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ____"
    missing_indices = [11]
    expected_phrases = [
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    ]

    result = find_missing_words(partial_mnemonic, missing_indices, show_progress=False)
    assert expected_phrases[0] in result


def test_successful_correction():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "recover",
            "--mnemonic",
            "volume prison sunset envelope office pool garlic want diet humble supr bean",
        ],
    )
    print(result.output)
    assert result.exit_code == 0
    assert "✅ Corrected 'supr' to 'super'" in result.output
    assert "✅ Mnemonic is complete and valid." in result.output


def test_main_command():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "recover",
            "--mnemonic",
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ____",
        ],
    )
    print(result.output)
    assert result.exit_code == 0
    assert (
        "❌ No missing words detected. Use '____' for missing ones."
        not in result.output
    )
    assert "✅ Found" in result.output
