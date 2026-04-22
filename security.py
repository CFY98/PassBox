# EXTERNAL IMPORTS
import os
import hashlib
from argon2 import PasswordHasher
from cryptography.fernet import Fernet

# PASSBOX IMPORTS
from config import KEY, VAULT

# ENCRYPTION FUNCTIONS
def generate_key():
    if not KEY.exists():
        key = Fernet.generate_key()
        KEY.write_bytes(key)

def encryption(value):
    key = KEY.read_bytes()
    cipher = Fernet(key)
    return cipher.encrypt(value.encode("utf-8")).decode("utf-8")


def decryption(value):
    key = KEY.read_bytes()
    cipher = Fernet(key)
    return cipher.decrypt(value.encode("utf-8")).decode("utf-8")

def hash_password(value):
    ph = PasswordHasher()
    return ph.hash(value)

def verify_password(hashed_value, value):
    try:
        return ph.verify(hash_password, value)
    except Exception:
        return False

def hash_domain(domain: str) -> str:
    domain = domain.strip().lower()
    return hashlib.sha256(domain.encode("utf-8")).hexdigest()
