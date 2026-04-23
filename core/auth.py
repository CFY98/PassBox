# EXTERNAL LIBRARIES
import csv
import os
import random
import string
import pwinput

# PASSBOX MODULES
from .security import ( _derive_master_key, derive_enc_key, derive_hmac_key, derive_app_key, encryption, decryption, hash_password, verify_password, derive_app_user)
from lib.config import (CREDENTIALS, APP_SALT, VAULT_DIR)
from app.session import Session

# AUTH CLASS
class Auth:
    def __init__(self):
        gen_app_salt(APP_SALT)
        self.credentials = {}
        if not CREDENTIALS.exists():
            with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["username_hmac", "username", "password", "hint", "vault_file"]
                )
                writer.writeheader()

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.credentials[row["username_hmac"]] = row

    def login(self, username, password):
        master_key = _derive_master_key(password, APP_SALT)
        enc_key = derive_enc_key(master_key)
        hmac_key = derive_hmac_key(master_key)
        app_key = derive_app_key(APP_SALT)

        username_hmac = derive_app_user(username, app_salt)
        if username_hmac not in self.credentials:
            return "invalid_user", None

        creds = self.credentials[username_hmac]
        if verify_password(creds["password"], password):
            vault_file = creds["vault_file"]
            return "valid", Session(enc_key, hmac_key, vault_file)
        return "invalid_password", None

    def get_hint(self, username):
        app_key = derive_app_key(APP_SALT)
        username_hmac = derive_app_user(username, app_key)
        
        creds = self.credentials.get(username_hmac)
        if creds:    
            return creds["hint"]
        return None

    def register(self, username, password, hint):
        master_key = _derive_master_key(password, APP_SALT)
        enc_key = derive_enc_key(master_key)
        hmac_key = derive_hmac_key(master_key)
        app_key = derive_app_key(APP_SALT)

        username_hmac = derive_app_user(username, app_key)
        if username_hmac in self.credentials:
            print("Username already exists.")
            return False
        
        vault_file = str(VAULT_DIR / f"{username_hmac[:16]}.json")
        record = { "username_hmac": username_hmac, "username": encryption(username, enc_key), "password": hash_password(password), "hint": encryption(hint, enc_key), "vault_file": vault_file}

        with open(CREDENTIALS, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=record.keys())
            writer.writerow(record)

        # UPDATE CACHE
        self.credentials[username_hmac] = record
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
        old_master = _derive_master_key(old_password, APP_SALT)
        old_hmac = derive_hmac_key(old_master)
        app_key = derive_app_key(APP_SALT)

        username_hmac = derive_app_user(username, app_key)
        
        new_master = _derive_master_key(new_password, APP_SALT)
        new_enc = derive_enc_key(new_master)
        new_hmac = derive_hmac_key(new_master)
        
        enc_username = encryption(username, app_key)
        enc_hint = encryption(new_hint, app_key)
        hash_pass = hash_password(new_password)
        
        # UPDATE PERSISTENT STORAGE
        updated_rows = []

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["username_hmac"] == username_hmac:
                    if hint is not None:
                        row["hint"] = enc_hint

                    row["username"] = enc_username
                    row["password"] = hash_pass

                updated_rows.append(row)
        
        with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

        # UPDATE CACHE
        if username_hmac in self.credentials:
            self.credentials[username_hmac]["username"] = enc_username
            self.credentials[username_hmac]["password"] = hash_pass
            if hint is not None:
                self.credentials[username_hmac]["hint"] = enc_hint

    def update_hint(self, username, password):
        to_update = pwinput.pwinput("Update memorable hint (y/n)? ").casefold().strip()
        if to_update == "n":
            return False
        new_hint = input("Please enter a hint: ")
        
        old_master = _derive_master_key(password, APP_SALT)
        old_hmac = derive_hmac_key(old_master)
        app_key = derive_app_key(APP_SALT)

        username_hmac = derive_app_user(username, app_key)
        
        new_master = _derive_master_key(password, app_key)
        new_enc = derive_enc_key(new_master)
        new_hmac = derive_hmac_key(new_master)
        
        enc_hint = encryption(hint, app_key)

        # UPDATE PERSISTENT STORAGE
        updated_rows = []

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["username_hmac"] == username_hmac:
                    row["hint"] = enc_hint

                updated_rows.append(row)
        
        with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

        # UPDATE CACHE
        if username_hmac in self.credentials:
            self.credentials[username_hmac]["hint"] = enc_hint
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
