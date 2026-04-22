# EXTERNAL LIBRARIES
import os
import hmac
import hashlib
import base64
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

# PASSBOX MODULES
from lib.config import CREDS_SALT

# SALT GENERATION
def generate_salt(path):
    if not path.exists():
        path.write_bytes(os.urandom(16))

# KEY DERIVATION
def derive_vault(value, salt):
    return _derive(value, salt)

def derive_creds(value):
    return _derive(value, CREDS_SALT.read_bytes())

def _derive(value, salt):
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

# HASHING FOR STABLE IDENTIFIERS
def check_key(path) -> bytes:
    if os.path.exists(path):
        return bytes.fromhex(open(path, "r", encoding="utf-8").read())

    domain_key = os.urandom(32)
    path.write_text(domain_key.hex(), encoding="utf-8")
    return domain_key

def hash_value(value: str, hmac_key: bytes) -> str:
    return hmac.new(hmac_key, value.strip().lower().encode("utf-8"),hashlib.sha256).hexdigest()

def derive_hmac_key(vault_key: bytes) -> bytes:
    return hashlib.sha256(vault_key).digest()
