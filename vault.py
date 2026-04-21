import json
import os

from cryptography.fernet import Fernet


def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as f:
            f.write(key)


def encryption(value):
    with open("key.key", "rb") as f:
        key = f.read()
    cipher = Fernet(key)
    return cipher.encrypt(value.encode("utf-8")).decode("utf-8")


def decryption(value):
    with open("key.key", "rb") as f:
        key = f.read()
    cipher = Fernet(key)
    return cipher.decrypt(value.encode("utf-8")).decode("utf-8")


def new_vault():
    with open("vault.json", "w") as f:
        json.dump({}, f)


def vault():
    if os.path.exists("vault.json"):
        with open("vault.json", "r") as f:
            return json.load(f)
    else:
        new_vault()
        return {}
