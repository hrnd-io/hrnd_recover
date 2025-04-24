import hashlib
import ecdsa
import base58


def generate_private_key(passphrase: str) -> bytes:
    """Generate a private key from a passphrase."""
    return hashlib.sha256(passphrase.encode("utf-8")).digest()


def generate_public_key(private_key: bytes) -> bytes:
    """Generate a public key from a private key using ECDSA."""
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return b"\x04" + vk.to_string()


def generate_bitcoin_address(public_key: bytes) -> str:
    """Generate a Bitcoin address from a public key."""
    # Perform SHA-256 hashing on the public key
    sha256_bpk = hashlib.sha256(public_key).digest()
    # Perform RIPEMD-160 hashing on the result of SHA-256
    ripemd160_bpk = hashlib.new("ripemd160", sha256_bpk).digest()
    # Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
    hashed_public_key = b"\x00" + ripemd160_bpk
    # Perform SHA-256 hash twice
    sha256_hashed_public_key = hashlib.sha256(hashed_public_key).digest()
    sha256_hashed_public_key = hashlib.sha256(sha256_hashed_public_key).digest()
    # Take the first 4 bytes of the second SHA-256 hash for checksum
    checksum = sha256_hashed_public_key[:4]
    # Add the 4 checksum bytes at the end of RIPEMD-160 hash
    binary_address = hashed_public_key + checksum
    # Convert the result to a base58 string
    address = base58.b58encode(binary_address)
    return address.decode("utf-8")
