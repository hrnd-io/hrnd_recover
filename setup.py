from setuptools import setup, find_packages

setup(
    name="hrnd",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["click", "mnemonic", "tqdm", "rapidfuzz", "bip-utils"],
    entry_points={"console_scripts": ["hrnd = hrnd.cli:cli"]},
)
