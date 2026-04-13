import json
import os

from cryptography.fernet import Fernet


def encryption(password):
    key = Fernet.generate_key()
    cipher = Fernet(key)

    enc_password = cipher.encrypt(password.encode("utf-8"))

    with open("key.key", "wb") as f:
        f.write(key)

    return enc_password


def decryption(enc_password):
    with open("key.key", "rb") as f:
        key = f.read()
    cipher = Fernet(key)
    dec_password = cipher.decrypt(enc_password).decode("utf-8")
    return dec_password


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
