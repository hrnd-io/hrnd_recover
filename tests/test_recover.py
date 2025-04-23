import pytest
from src.recover import find_missing_words
from click.testing import CliRunner
from src.recover import main


def test_find_missing_words():
    partial_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ____"
    missing_indices = [11]
    expected_phrases = [
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    ]

    result = find_missing_words(partial_mnemonic, missing_indices, show_progress=False)
    assert expected_phrases[0] in result


def test_main_command():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--mnemonic",
            "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ____",
        ],
    )
    assert result.exit_code == 0
    assert "✅ Found" in result.output
