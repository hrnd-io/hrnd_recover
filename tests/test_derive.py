import os
import sys
import pytest

# Add the project root to the system path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.derive.mnemonic_phrase import derive_wallet_info
from src.derive.brain_wallet import (
    generate_private_key,
    generate_public_key,
    generate_bitcoin_address,
)

# Constants for test vectors
mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

# Test vector: mnemonic, expected address, format, index, path
test_vectors = [
    # Legacy via custom path
    (mnemonic, "13iX7DteNj1gV7zhe4t6o9FX9CArR5wZxz", "legacy", 0, "m/0/0"),
    # BIP84 (SegWit)
    (mnemonic, "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu", "segwit", 0, None),
    # BIP86 (Taproot)
    (
        mnemonic,
        "bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr",
        "taproot",
        0,
        None,
    ),
]


class TestMnemonicDerivation:
    @pytest.mark.mnemonics
    @pytest.mark.parametrize(
        "mnemonic, expected_address, fmt, index, path", test_vectors
    )
    def test_address_derivation(self, mnemonic, expected_address, fmt, index, path):
        """
        Test the address derivation for different formats and paths.
        """
        result = derive_wallet_info(
            mnemonic, index=index, fmt=fmt, show_xpub=False, path=path
        )
        assert result == expected_address


class TestBrainWalletDerivation:
    @pytest.mark.brainwallet
    def test_brain_wallet_address_derivation(self):
        """
        Test the address derivation from a brain wallet passphrase.
        """
        passphrase = "Satoshi Nakamoto"
        expected_address = "1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW"

        private_key = generate_private_key(passphrase)
        public_key = generate_public_key(private_key)
        bitcoin_address = generate_bitcoin_address(public_key)

        assert bitcoin_address == expected_address
