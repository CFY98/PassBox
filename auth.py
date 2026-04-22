# EXTERNAL MODULES
import csv
import os
import random
import string
import pandas as pd
import pwinput

# PASSBOX MODULES
from security import (derive_creds, derive_vault, decryption, encryption, generate_salt, hash_password, verify_password)
from config import CREDENTIALS

# AUTH CLASS
class Auth:
    def __init__(self):
        generate_salt(CREDENTIALS)
        self.credentials = {}
        if not CREDENTIALS.exists():
            with open(CREDENTIALS, "w", newline="") as master_password:
                writer = csv.DictWriter(
                    master_password, fieldnames=["username", "password", "hint"]
                )
                writer.writeheader()

        with open(CREDENTIALS, "r", newline="") as master_password:
            reader = csv.DictReader(master_password)
            for row in reader:
                self.credentials[row["username"]] = {
                    "password": row["password"],
                    "hint": row["hint"],
                }

    def login(self, username, password):
        cred = derive_creds(password)
        for enc_username, creds in self.credentials.items():
            try:
                dec_username = decryption(enc_username, cred)
            except Exception:
                    continue

            if dec_username == username:
                if verify_password(creds["password"], password):
                    return "success", derive_vault(password)
                return "Incorrect password, please try again", None
        return "User not found", None        

    def get_hint(self, username, key):
        for enc_username, creds in self.credentials.items():
            try:
                if decryption(enc_username, key) == username:
                    return f"Hint: {self.credentials[username]['hint'].strip()}"
            except Exception:
                continue
        return None

    def register(self, username, password, hint):
        key = derive_creds(password)
        if any(decryption(u, key) == username for u in self.credentials):
            print("Username already exists.")
            return False
        with open(CREDENTIALS, "a", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["username", "password", "hint"]
            )
            writer.writerow(
                {
                    "username": encryption(username, key),
                    "password": hash_password(password),
                    "hint": encryption(hint, key),
                }
            )
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

    def update_password(self, username, old_password, new_password):
        key = derive_creds(old_password)
        new_key = derive_creds(new_password)
        df = pd.read_csv(CREDENTIALS)
        for i, row in df.iterrows():
            try:
                if decryption(row["username"], key) == username:
                    df.at[i, "username"] = encryption(username, new_key)
                    df.at[i, "password"] = hash_password(new_password)
                    df.at[i, "hint"] = encryption(decryption(row["hint"], key), new_key)
                    break
            except Exception:
                continue
        df.to_csv(CREDENTIALS, index=False)

    def update_hint(self, username, key):
        to_update = input("Update memorable hint (Yes/No)? ").casefold().strip()
        if to_update == "no":
            return False
        new_hint = input("Please enter a hint: ")
        df = pd.read_csv(CREDENTIALS)
        for i, row in df.iterrows():
            try:
                if decryption(row["username"], key) == username:
                    df.at[i, "hint"] = encryption(new_hint, key)
                    break
            except Exception:
                continue
        df.to_csv(CREDENTIALS, index=False)
        return True

    def change_password(self, username, password):
        while True:
            choice = input("Change password (Yes/No)? ").strip().lower()

            if choice == "yes":
                suggestion = self.strong_password(15)
                print(
                    f"Password suggestion: {suggestion}\n",
                    end="",
                )

                use_suggestion = input("Use suggestion (Yes/No)?" ).strip().casefold()
                if use_suggestion == "yes":
                    self.update_password(username, password, suggestion)
                    self.update_hint(username, derive_creds(suggestion))
                    return suggestion
                
                update = pwinput.pwinput("Please enter new password: ")

                if update == password:
                    print("Cannot be old password, please try again.")
                    continue

                if update == "h3110 w0r1d!!":
                    self.update_password(username, update)
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
                self.update_hint(username, derive_creds(update))
                print("The password was succesfully updated")
                return update

            elif choice == "no":
                print("The password was not updated")
                return password

            else:
                retry = input("Did I catch that right (Yes/No)? ").strip().lower()
                if retry == "yes":
                    return password
                elif retry != "no":
                    print('It\'s a "Yes" or "No" answer.')
                else:
                    continue
