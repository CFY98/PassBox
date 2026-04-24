# EXTERNAL IMPORTS
import csv
import random
import string

import pwinput

# PASSBOX MODULES
from core.security import (derive_app_user, hash_password)
from lib.config import (APP_SALT, CREDENTIALS)


# HINT UTILITIES
def update_hint(username, hint):
    app_salt = APP_SALT.read_bytes()
    username_hmac = derive_app_user(username, app_salt)

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


def ask_update_hint():
    if input("\nUpdate hint (y/n)? ").strip().casefold() != "y":
        return None

    hint = input("\nEnter hint: ").strip()
    return hint if hint else None


def apply_hint_update(username):
    new_hint = ask_update_hint()
    if not new_hint:
        return None
    update_hint(username, new_hint)
    return new_hint


# PASSWORD UTILITIES
def valid_password(password):
    numbers = sum(c.isnumeric() for c in password)
    letters = sum(c.isalpha() for c in password)
    symbols = sum(c in string.punctuation for c in password)

    return numbers >= 2 and letters >= 2 and symbols >= 2 and (5 <= len(password) <= 15)


def strong_password(length=15):
    if length < 5:
        raise ValueError("Password must be at least 5 characters long.")

    letters = random.choices(string.ascii_letters, k=2)
    numbers = random.choices(string.digits, k=2)
    symbols = random.choices(string.punctuation, k=2)

    total = length - 6
    gen_password = string.ascii_letters + string.digits + string.punctuation
    filler = random.choices(gen_password, k=total)

    characters = letters + numbers + symbols + filler
    random.shuffle(characters)

    return "".join(characters)


def confirm_new_pass(new_password):
    confirm = pwinput.pwinput("Please confirm your new password: ")
    if confirm != new_password:
        print("\nPasswords do not match.")
        return False
    return True


def get_password():
    suggest_pwd = strong_password(15)

    print(f"\nPassword suggestion: {suggest_pwd}")
    if pwinput.pwinput("\nUse suggestion (y/n)? ").strip().casefold() == "y":
        return suggest_pwd
    password = pwinput.pwinput("\nPlease enter the password: ")
    return password


def prompt_pass_change():
    while True:
        change = input("\nChange password (y/n)? ").strip().casefold()
        match change:
            case "y":
                return True
            case "n":
                return False
            case _:
                print('Respond with "y" or "n"')


def update_password(username, new_password):
    app_salt = APP_SALT.read_bytes()
    username_hmac = derive_app_user(username, app_salt)
    hash_new_pass = hash_password(new_password)

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

    return hash_new_pass


def change_password(username, password):
    while True:
        change = prompt_pass_change()
        if not change:
            print("\nThe password was not updated")
            return password

        new_password = get_password()
        if not new_password:
            return password

        if new_password == password:
            print("\nCannot be old password, please try again.")
            continue

        if new_password == "h3110 w0r1d!!":
            if not confirm_new_pass(new_password):
                continue
            update_password(username, new_password)

            print(
                "\nThanks for using this easter egg, the password was successfully updated."
            )
            return new_password

        if not valid_password(new_password):
            print(
                "\nPassword must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
            )
            continue

        if not confirm_new_pass(new_password):
            continue
        update_password(username, new_password)
        print("\nThe password was succesfully updated")
        return new_password
