# EXTERNAL MODULES
import csv
import os
import random
import string

import pandas as pd
import pwinput

# PASSBOX MODULES
from utils import decryption, encryption, generate_key
from main import interface

# AUTH START
class Auth:
    def __init__(self):
        generate_key()
        self.credentials = {}
        if not os.path.exists("credentials.csv"):
            with open("credentials.csv", "w", newline="") as master_password:
                writer = csv.DictWriter(
                    master_password, fieldnames=["username", "password", "hint"]
                )
                writer.writeheader()

        with open("credentials.csv", "r", newline="") as master_password:
            reader = csv.DictReader(master_password)
            for row in reader:
                self.credentials[decryption(row["username"])] = {
                    "password": decryption(row["password"]),
                    "hint": decryption(row["hint"]),
                }

    def login(self, username, password):
        if username not in self.credentials.keys():
            return "Login details not found"
        if self.credentials[username]["password"] != password:
            return "Incorrect password, please try again"
        return True

    def get_hint(self, username):
        if username in self.credentials:
            return f"Hint: {self.credentials[username]['hint'].strip()}"

    def register(self, username, password, hint):
        if username in self.credentials:
            print("Username already exists.")
            return False
        with open("credentials.csv", "a", newline="") as master_password:
            writer = csv.DictWriter(
                master_password, fieldnames=["username", "password", "hint"]
            )
            writer.writerow(
                {
                    "username": encryption(username),
                    "password": encryption(password),
                    "hint": encryption(hint),
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

    def update_password(self, username, password):
        df = pd.read_csv("credentials.csv")
        for i, row in df.iterrows():
            if decryption(row["username"]) == username:
                df.at[i, "password"] = encryption(password)
                break
        df.to_csv("credentials.csv", index=False)
        self.credentials[username]["password"] = password

    def update_hint(self, username):
        to_update = input("Update memorable hint (Yes/No)? ").casefold().strip()
        if to_update == "no":
            return False
        new_hint = input("Please enter a hint: ")
        df = pd.read_csv("credentials.csv")
        for i, row in df.iterrows():
            if decryption(row["username"]) == username:
                df.at[i, "hint"] = encryption(new_hint)
                break
        df.to_csv("credentials.csv", index=False)
        self.credentials[username]["hint"] = new_hint
        return True

    def change_password(self, username, password):
        while True:
            choice = input("Change password (Yes/No)? ").strip().lower()

            if choice == "yes":
                suggestion = self.strong_password(15)
                print(
                    f'Here is a suggestion: {suggestion}\nIf you want to use it, type "use suggestion".\n',
                    end="",
                )

                update = pwinput.pwinput("Please enter new password: ")
                if update == "use suggestion":
                    self.update_password(username, suggestion)
                    self.update_hint(username)
                    return suggestion

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

                self.update_password(username, update)
                self.update_hint(username)
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
