# EXTERNAL LIBRARIES
import csv
import os
import random
import string
import pandas as pd
import pwinput

# PASSBOX MODULES
from .security import ( _derive, encryption, decryption, hash_password, verify_password, hash_value)
from lib.config import (CREDENTIALS, APP_SALT, VAULT_DIR)
from app.session import Session

# AUTH CLASS
class Auth:
    def __init__(self):
        self.credentials = {}
        if not CREDENTIALS.exists():
            with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["username_hmac", "user_salt", "username", "password", "hint", "vault_salt", "vault_file"]
                )
                writer.writeheader()

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.credentials[row["username_hmac"]] = {"user_salt": row["user_salt"], "username": row["username"], "password": row["password"], "hint": row["hint"], "vault_salt": row["vault_salt"], "vault_file": row["vault_file"]}

    def login(self, username, password):
        lookup_salt = _derive(username, APP_SALT)
        username_hmac = hash_value(username, get_hmac_key(password, bytes.fromhex(lookup_salt)))
        if username_hmac not in self.credentials:
            return "invalid_user", None

        creds = self.credentials[username_hmac]
        if verify_password(creds["password"], password):
            vault_salt = bytes.fromhex(creds["vault_salt"])
            master_key = _derive(password, vault_salt)
            vault_file = creds["vault_file"]
            return "valid", Session(self, master_key, vault_file)
        return "invalid_password", None

    def get_hint(self, username, key):
        lookup_salt = _derive(username, APP_SALT)
        username_hmac = hash_value(username, get_hmac_key(username, lookup_salt))
        creds = self.credentials.get(username_hmac)
        if creds:    
            return f"Hint: {creds['hint'].strip()}"
        return None

    def register(self, username, password, hint):
        user_salt = os.urandom(16).hex()
        username_hmac = hash_value(username, get_hmac_key(password, bytes.fromhex(user_salt)))
        if username_hmac in self.credentials:
            print("Username already exists.")
            return False
        key = _derive(password, bytes.fromhex(user_salt))
        vault_salt = os.urandom(16).hex()
        vault_file = str(VAULT_DIR / f"{username_hmac[:16]}.json")
        with open(CREDENTIALS, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["username_hmac", "user_salt", "username", "password", "hint", "vault_salt", "vault_file"]
            )
            writer.writerow(
                {
                    "username_hmac": username_hmac,
                    "user_salt": user_salt,
                    "username": encryption(username, key),
                    "password": hash_password(password),
                    "hint": hint,
                    "vault_salt": vault_salt,
                    "vault_file": vault_file
                }
            )
        self.credentials[username_hmac] = {"username": encryption(username, key), "password": hash_password(password), "hint": encryption(hint, key), "vault_salt": vault_salt, "vault_file": vault_file}
        return True

    def logout(self):
        self.credentials = {}

    def valid_password(self, password):
        numbers = sum(c.isnumeric() for c in password)
        letters = sum(c.isalpha() for c in password)
        symbols = sum(c in string.punctuation for c in password)

        return (
            numbers >= 2
            and letters >= 2
            and symbols >= 2
            and (5 <= len(password) <= 15)
        )

    def strong_password(self, length=15):
        if length < 5:
            raise ValueError("Password must be at least 5 characters long.")

        letters = random.choices(string.ascii_letters, k=2)
        numbers = random.choices(string.digits, k=2)
        symbols = random.choices(string.punctuation, k=2)

        total = length - 6
        valid_password = string.ascii_letters + string.digits + string.punctuation
        filler = random.choices(valid_password, k=total)

        characters = letters + numbers + symbols + filler
        random.shuffle(characters)

        return "".join(characters)

    def update_password(self, username, old_password, new_password, hint=None):
        lookup_salt = _derive(username, APP_SALT)
        username_hmac = hash_value(username, get_hmac_key(old_password, lookup_salt))
        
        df = pd.read_csv(CREDENTIALS)
        for i, row in df.iterrows():
            if row["username_hmac"] == username_hmac:
                if hint is not none:
                    df.at[i, "hint"] = hint
                user_salt = bytes.fromhex(row["user_salt"])
                new_key = _derive(new_password, user_salt)
                df.at[i, "username"] = encryption(username, new_key)
                df.at[i, "password"] = hash_password(new_password)
                break
        df.to_csv(CREDENTIALS, index=False)

        if username_hmac in self.credentials:
            self.credentials[username_hmac]["username"] = encryption(username, new_key)
            self.credentials[username_hmac]["password"] = hash_password(new_password)
            if hint is not None:
                self.credentials[username_hmac]["hint"] = hint

    def update_hint(self, username):
        to_update = pwinput.pwinput("Update memorable hint (y/n)? ").casefold().strip()
        if to_update == "n":
            return False
        new_hint = input("Please enter a hint: ")
        lookup_dalt = _derive(username, APP_SALT)
        username_hmac = hash_value(username, get_hmac_key(old_password, lookup_salt))
        df = pd.read_csv(CREDENTIALS)
        for i, row in df.iterrows():
            if row["username_hmac"] == username_hmac:
                df.at[i, "hint"] = new_hint
                break
        df.to_csv(CREDENTIALS, index=False)
        
        if username_hmac in self.credentials:
            self.credentials[username_hmac]["hint"] = new_hint
        return True

    def change_password(self, username, password):
        while True:
            choice = input("Change password (y/n)? ").strip().lower()

            if choice == "y":
                suggestion = self.strong_password(15)
                print(
                    f"Password suggestion: {suggestion}\n",
                    end="",
                )

                use_suggestion = pwinput.pwinput("Use suggestion (y/n)? ").strip().casefold()
                if use_suggestion == "y":
                    self.update_password(username, password, suggestion)
                    self.update_hint(username)
                    return suggestion
                
                update = pwinput.pwinput("Please enter new password: ")

                if update == password:
                    print("Cannot be old password, please try again.")
                    continue

                if update == "h3110 w0r1d!!":
                    self.update_password(username, password, update)
                    self.update_hint(username)
                    print(
                        "Thanks for using this easter egg, the password was successfully updated."
                    )
                    return update

                if not self.valid_password(update):
                    print(
                        "Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
                    )
                    continue

                confirm = pwinput.pwinput("Please confirm your new password: ")
                if confirm != update:
                    print("Passwords do not match. Try again.")
                    continue

                self.update_password(username, password, update)
                self.update_hint(username)
                print("The password was succesfully updated")
                return update

            elif choice == "n":
                print("The password was not updated")
                return password

            else:
                retry = input("Did I catch that right (y/n)? ").strip().lower()
                if retry == "y":
                    return password
                elif retry != "n":
                    print("Invalid input, please try again.")
                else:
                    continue
