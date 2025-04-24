# HRND — Hardened Bitcoin Key Recovery

**HRND** (pronounced "hardened") is a CLI tool suite to help users securely recover lost or incomplete Bitcoin wallet mnemonics and derive addresses or xpubs. It combines a brute-force recovery engine, AI-assisted typo correction, and a modular CLI for seamless usage.

---

## 📦 Installation

### From GitHub (Editable Mode)

```bash
# Clone the repository
git clone https://github.com/<your-username>/hrnd_recover.git
cd hrnd_recover

# Create and activate Python venv
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies and the CLI tool in editable mode
pip install --upgrade pip
pip install -e .
```

---

## ⚙️ Commands

Once installed, the `hrnd` command is available globally.

### `hrnd recover`
Recover valid mnemonics by brute-forcing missing or placeholder words.

```bash
# Basic usage with placeholders '____'
hrnd recover --mnemonic "abandon abandon ____ abandon abandon abandon abandon abandon abandon abandon abandon about"

# Suppress detailed output (keep progress bar)
hrnd recover --mnemonic "..." --quiet

# Save results to a file
hrnd recover --mnemonic "..." --output recovered.txt
```

### `hrnd derive`
A grouped command for address and xpub derivation.

#### `hrnd derive mnemonic-phrase`
Derive a Bitcoin address or xpub from a full mnemonic.

```bash
# Derive a legacy address (default)
hrnd derive mnemonic-phrase --mnemonic "abandon abandon ... about"

# Derive a SegWit (Bech32) address
hrnd derive mnemonic-phrase -m "..." --format segwit

# Get the account xpub
hrnd derive mnemonic-phrase -m "..." --xpub
```

#### `hrnd derive brain-wallet`
Generate a Bitcoin address directly from a passphrase (brain wallet).

```bash
hrnd derive brain-wallet --passphrase "correct horse battery staple"
```

---

## 🛠 Development

- Project uses a `src/` layout for Python packaging.
- CLI entry point: `hrnd/cli.py`
- Recovery logic: `hrnd/recover.py`
- Derivation subcommands: `src/derive/`

### Running Tests

```bash
pytest
```

---

## 🚚 Releases & Packaging

- Use `setup.py` and `setuptools` for packaging.
- To create a GitHub release:
  1. Tag a version: `git tag v0.1.0`
  2. Push tags: `git push --tags`
  3. Draft a release on GitHub with changelog.

- To publish to PyPI (future):
  1. Build: `python setup.py sdist bdist_wheel`
  2. Upload: `twine upload dist/*`

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests to improve features, add new commands, or enhance tests.

---

## 📄 License

This project is licensed under the MIT License.

