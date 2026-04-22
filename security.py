# EXTERNAL IMPORTS
import os
import hashlib
import base64
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

# PASSBOX IMPORTS
from config import VAULT_SALT, CREDS_SALT

# SALT GENERATION
def generate_salt(path):
    if not path.exists():
        path.write_bytes(os.urandom(16))

def load_salt():
    return CREDS_SALT.read_bytes()

# KEY DERIVATION
def derive_vault(value):
    return _derive(value, VAULT_SALT)

def derive_creds(value):
    return _derive(value, CREDS_SALT)

def _derive(value, salt_path):
    if not salt_path.exists():
        salt_path.write_bytes(os.urandom(16))

    salt = load_salt()

    kdf = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=64*1024, ad=None, secret=None,)
    return base64.urlsafe_b64encode(kdf.derive(value.encode("utf-8")))

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

def hash_domain(domain: str) -> str:
    domain = domain.strip().lower()
    return hashlib.sha256(domain.encode("utf-8")).hexdigest()
