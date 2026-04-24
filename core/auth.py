# EXTERNAL LIBRARIES
import csv
import os

from app.session import Session
from lib.config import APP_SALT, CREDENTIALS, VAULT_DIR

# PASSBOX MODULES
from .security import (
    _derive_master_key,
    derive_app_user,
    derive_user_enc_key,
    encryption,
    gen_app_salt,
    hash_password,
    verify_password,
)


# AUTH CLASS
class Auth:
    def __init__(self):
        gen_app_salt(APP_SALT)
        self.app_salt = APP_SALT.read_bytes()

        self.credentials = {}
        if not CREDENTIALS.exists():
            with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "username_hmac",
                        "user_salt",
                        "username",
                        "password",
                        "hint",
                        "vault_file",
                    ],
                )
                writer.writeheader()

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.credentials[row["username_hmac"]] = row

    def login(self, username, password):
        username_hmac = derive_app_user(username, self.app_salt)
        creds = self.credentials.get(username_hmac)
        if not creds:
            return "invalid_user", None

        if not verify_password(creds["password"], password):
            return "invalid_password", None

        user_salt = bytes.fromhex(creds["user_salt"])
        master_key = _derive_master_key(password, user_salt)
        vault_file = creds["vault_file"]
        return "valid", Session(master_key, vault_file)

    def get_hint(self, username):
        username_hmac = derive_app_user(username, self.app_salt)
        creds = self.credentials.get(username_hmac)

        if not creds:
            return None
        return creds["hint"]

    def register(self, username, password, hint):
        username_hmac = derive_app_user(username, self.app_salt)
        if username_hmac in self.credentials:
            print("Username already exists.")
            return False

        user_salt = os.urandom(16)
        master_key = _derive_master_key(password, user_salt)
        user_enc_key = derive_user_enc_key(master_key)

        vault_file = str(VAULT_DIR / f"{username_hmac[:16]}.json")
        record = {
            "username_hmac": username_hmac,
            "user_salt": user_salt.hex(),
            "username": encryption(username, user_enc_key),
            "password": hash_password(password),
            "hint": hint,
            "vault_file": vault_file,
        }

        with open(CREDENTIALS, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            writer.writerow(record)

        # UPDATE CACHE
        self.credentials[username_hmac] = record
        return True

    def update_cache_pass(self, username, new_password):
        username_hmac = derive_app_user(username, self.app_salt)
        creds = self.credentials.get(username_hmac)

        if not creds:
            return False

        self.credentials[username_hmac]["password"] = new_password
        return True

    def update_cache_hint(self, username, new_hint):
        username_hmac = derive_app_user(username, self.app_salt)
        creds = self.credentials.get(username_hmac)

        if not creds:
            return False

        self.credentials[username_hmac]["password"] = new_hint
        return True

    def logout(self):
        self.credentials = {}
