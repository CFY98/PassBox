# EXTERNAL IMPORTS
import json
import os
import hashlib

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

def hash_domain(domain: str) -> str:
    domain = domain.strip().lower()
    return hashlib.sha256(domain.encode("utf-8")).hexdigest()

# VAULT FUNCTIONS
def new_vault():
    VAULT.write_text(json.dumps({}), encoding="utf-8")


def vault():
    if VAULT.exists():
            try:
                return json.load(VAULT.read_text())
            except json.JSONDecodeError:
                return {}
    else:
        new_vault()
        return {}
