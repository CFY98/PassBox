import csv
import os

from vault import encryption, vault


class Auth:
    def __init__(self):
        self.credentials = {}
        if not os.path.exists("credentials.csv"):
            with open("credentials.csv", "w", newline="") as master_password:
                writer = csv.DictWriter(
                    master_password, fieldnames=["username", "password"]
                )
                writer.writeheader()

        with open("credentials.csv", "r", newline="") as master_password:
            reader = csv.DictReader(master_password)
            for row in reader:
                self.credentials[row["username"]] = row["password"]

    def login(self, username, password):
        if username not in self.credentials.keys():
            return "Username not found"
        elif self.credentials[username] != password:
            return "Incorrect password, please try again"
        return vault()

    def register(self, username, password):
        if username in self.credentials:
            print("Username already exists.")
            return False
        with open("credentials.csv", "a", newline="") as master_password:
            writer = csv.DictWriter(
                master_password, fieldnames=["username", "password"]
            )
            writer.writerow({"username": username, "password": password})
            return writer

    def logout(self):
        self.credentials = {}
