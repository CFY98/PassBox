# EXTERNAL LIBRARIES
import csv
import os
import pwinput

# PASSBOX MODULES
from .security import (gen_app_salt, get_app_salt, _derive_master_key, derive_user_enc_key, derive_app_user, encryption, hash_password, verify_password)
from .utils import (valid_password, strong_password)
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
                    f, fieldnames=["username_hmac", "user_salt", "username", "password", "hint", "vault_file"]
                )
                writer.writeheader()

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.credentials[row["username_hmac"]] = row

    def login(self, username, password):
        username_hmac = derive_app_user(username, get_app_salt())
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
        username_hmac = derive_app_user(username, get_app_salt())
        creds = self.credentials.get(username_hmac)
        
        if not creds:
            return None
        return creds["hint"]

    def register(self, username, password, hint):
        username_hmac = derive_app_user(username, get_app_salt())
        if username_hmac in self.credentials:
            print("Username already exists.")
            return False
        
        user_salt = os.urandom(16)
        master_key = _derive_master_key(password, user_salt)
        user_enc_key = derive_user_enc_key(get_app_salt())

        vault_file = str(VAULT_DIR / f"{username_hmac[:16]}.json")
        record = { "username_hmac": username_hmac, "user_salt": user_salt.hex(), "username": encryption(username, user_enc_key), "password": hash_password(password), "hint": hint, "vault_file": vault_file}

        with open(CREDENTIALS, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=record.keys())
            writer.writerow(record)

        # UPDATE CACHE
        self.credentials[username_hmac] = record
        return True

    def logout(self):
        self.credentials = {}


    def update_password(self, username, old_password, new_password):
        username_hmac = derive_app_user(username, get_app_salt())
        creds = self.credentials.get(username_hmac)
        
        if not creds:
            return False
        
        hash_new_pass = hash_password(new_password)
        
        # UPDATE PERSISTENT STORAGE
        updated_rows = []

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["username_hmac"] == username_hmac:
                    row["password"] = hash_new_pass
                updated_rows.append(row)
        
        with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

        # UPDATE CACHE
        self.credentials[username_hmac]["password"] = hash_new_pass
        return True

    def update_hint(self, username, hint):
        username_hmac = derive_app_user(username, get_app_salt())
        creds = self.credentials.get(username_hmac)
       
        if not creds:
            return False

        # UPDATE PERSISTENT STORAGE
        updated_rows = []

        with open(CREDENTIALS, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["username_hmac"] == username_hmac:
                    row["hint"] = hint

                updated_rows.append(row)
        
        with open(CREDENTIALS, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

        # UPDATE CACHE
        self.credentials[username_hmac]["hint"] = hint
        return True

    def ask_update_hint(self):
        if pwinput.pwinput("Update hint (y/n)? ").strip().casefold() != "y":
            return None
        
        hint = input("Enter hint: ").strip()
        return hint if hint else None

    def apply_hint_update(self, username):
        new_hint = self.ask_update_hint()
        if not new_hint:
            return False
        self.update_hint(username, new_hint)

    def change_password(self, username, password):
        while True:
            choice = input("Change password (y/n)? ").strip().lower()

            if choice == "y":
                suggestion = strong_password(15)
                print(
                    f"Password suggestion: {suggestion}\n",
                    end="",
                )

                use_suggestion = pwinput.pwinput("Use suggestion (y/n)? ").strip().casefold()
                if use_suggestion == "y":
                    self.update_password(username, password, suggestion)
                    self.apply_hint_update(username)
                    return suggestion
                
                update = pwinput.pwinput("Please enter new password: ")

                if update == password:
                    print("Cannot be old password, please try again.")
                    continue

                if update == "h3110 w0r1d!!":
                    self.update_password(username, password, update)
                    self.apply_hint_update(username)
                    print(
                        "Thanks for using this easter egg, the password was successfully updated."
                    )
                    return update

                if not valid_password(update):
                    print(
                        "Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
                    )
                    continue

                confirm = pwinput.pwinput("Please confirm your new password: ")
                if confirm != update:
                    print("Passwords do not match. Try again.")
                    continue

                self.update_password(username, password, update)
                self.apply_hint_update(username)
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
