# EXTERNAL LIBRARIES
import os
import hmac
import hashlib
import base64
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

# KEY DERIVATION
def _derive(value: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """
    Returns (derived_key, salt).
    - Pass salt=None when creating a new credential.
    - Pass the stored salt when re-deriving for verification/decryption.
    - Combines the generate_salt and derive_creds functions
    """

    if salt is None:
        salt = os.urandom(16).hex()

    kdf = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=64*1024, ad=None, secret=None,)
    key = base64.urlsafe_b64encode(kdf.derive(value.encode("utf-8")))

    return salt, key

# ENCRYPTION
def encryption(value, key):
    cipher = Fernet(key)
    return cipher.encrypt(value.encode("utf-8")).decode("utf-8")


def decryption(value, key):
    cipher = Fernet(key)
    return cipher.decrypt(value.encode("utf-8")).decode("utf-8")

def hash_password(value):
    return PasswordHasher().hash(value)

def verify_password(hashed_value, value):
    try:
        return PasswordHasher().verify(hashed_value, value)
    except Exception:
        return False

# HASHING FOR STABLE IDENTIFIERS
def get_hmac_key(value: str, salt: bytes) -> bytes:
    key, _ = derive_key(value, salt)
    return key

def hash_value(value: str, hmac_key: bytes) -> str:
    return hmac.new(hmac_key, value.strip().lower().encode("utf-8"),hashlib.sha256).hexdigest()

