# EXTERNAL LIBRARIES
import os
import hmac
import hashlib
import base64
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

# PASSBOX MODULES
from lib.config import APP_SALT

# GENERATE APP_SALT
def gen_app_salt(path):
    if not path.exists():
        path.write_bytes(os.urandom(16))

# KEY DERIVATION
def _derive_master_key(password: str, app_salt: bytes) -> bytes:
    kdf = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=64*1024, ad=None, secret=None,)
    return base64.urlsafe_b64encode(kdf.derive(value.encode("utf-8")))

def derive_enc_key(master_key):
    raw = hashlib.sha256(master_key + b"enc").digest()
    return base64.urlsafe_b64encode(raw)

def derive_hmac_key(master_key):
    return hashlib.sha256(master_key + b"hmac").digest()

def derive_app_user(value: str, app_salt: bytes) -> str:
    return hmac.new(app_salt, value.strip().lower().encode("utf-8"),hashlib.sha256).hexdigest()

def derive_app_key(app_salt: bytes):
    raw = hashlib.sha256(app_salt + b"app-key").digest()
    return base64.urlsafe_b64encode(raw)

# ENCRYPTION
def encryption(value, enc_key):
    cipher = Fernet(enc_key)
    return cipher.encrypt(value.encode("utf-8")).decode("utf-8")

def decryption(value, enc_key):
    cipher = Fernet(enc_key)
    return cipher.decrypt(value.encode("utf-8")).decode("utf-8")

# PASSWORD HASHING
def hash_password(value):
    return PasswordHasher().hash(value)

def verify_password(hashed_value, value):
    try:
        return PasswordHasher().verify(hashed_value, value)
    except Exception:
        return False

