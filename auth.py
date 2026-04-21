import csv
import os
import random
import string

import pandas as pd
import pwinput

from vault import encryption, vault


class Auth:
    def __init__(self):
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
                self.credentials[row["username"]] = row["password"]

    def login(self, username, password):
        if username not in self.credentials.keys():
            return "Login details not found"
        elif self.credentials[username] != password:
            return "Incorrect password, please try again"
        return vault()

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
        df.loc[df["username"] == username, "password"] = password
        df.to_csv("credentials.csv", index=False)

    def change_password(self, username, password):
        while True:
            choice = input("Change password? Yes/No: ").strip().lower()

            if choice == "yes":
                suggestion = self.strong_password(15)
                print(
                    f'Here is a suggestion: {suggestion}\nIf you want to use it, type "use suggestion".\n',
                    end="",
                )
                update = pwinput.pwinput("Please enter new password: ")

                if update == "use suggestion":
                    self.update_password(username, suggestion)
                    return suggestion

                confirm = pwinput.pwinput("Please confirm your new password: ")
                if confirm != update:
                    print("Passwords do not match. Try again.")
                    continue

                if update == password:
                    print("Cannot be old password, please try again.")
                    continue

                if update == "h3110 w0r1d!!":
                    self.update_password(username, update)
                    print(
                        "Thanks for using this easter egg, the password was successfully updated."
                    )
                    return update

                if not self.valid_password(update):
                    print(
                        "Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
                    )
                    continue

                self.update_password(username, update)
                print("The password was succesfully updated")
                return update

            elif choice == "no":
                print("No worries~")
                return password

            else:
                retry = input("Did I catch that right? Yes/No: ").strip().lower()
                if retry == "yes":
                    return password
                elif retry != "no":
                    print('It\'s a "yes" or "no" answer.')
                else:
                    continue

    def register(self, username, password, hint):
        if username in self.credentials:
            print("Username already exists.")
            return False
        with open("credentials.csv", "a", newline="") as master_password:
            writer = csv.DictWriter(
                master_password, fieldnames=["username", "password", "hint"]
            )
            writer.writerow({"username": username, "password": password, "hint": hint})
            return True

    def logout(self):
        self.credentials = {}
