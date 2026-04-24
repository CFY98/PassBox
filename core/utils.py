# EXTERNAL IMPORTS
import random
import string
import csv
import pwinput

# PASSBOX MODULES
from lib.config import CREDENTIALS, APP_SALT
from core.security import derive_app_user

# HINT UTILITIES
def update_hint(username, hint):
    app_salt = APP_SALT.read_bytes()
    username_hmac = derive_app_user(username, app_salt)

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
    valid_password = string.ascii_letters + string.digits + string.punctuation
    filler = random.choices(valid_password, k=total)

    characters = letters + numbers + symbols + filler
    random.shuffle(characters)

    return "".join(characters)


def get_password():
    suggest_pwd = strong_password(15)

    print(f"\nPassword suggestion: {suggest_pwd}")
    if pwinput.pwinput("\nUse suggestion (y/n)? ").strip().casefold() == "y":
        return suggest_pwd
    password = pwinput.pwinput("Please enter the password: ")
    return password


def confirm_new_pass():
    return pwinput.pwinput("Please confirm your new password: ")


def prompt_pass_change():
    while True
        change = input("Change password (y/n)? ").strip().casefold()
        match change:
            case "y":
                return True
            case "n":
                return False
            case _:
                print('Respond with "y" or "n"')


def change_password(username, password):
    while True:
        to_change = prompt_pass_change()
        if not to_change:
            print("The password was not updated")
            return password

        new_password = get_password()
        if not new_password:
            return password

        if new_password == password:
            print("Cannot be old password, please try again.")
            continue

        if new_password == "h3110 w0r1d!!":
            update_password(username, new_password)
            apply_hint_update(username)
            print(
                "Thanks for using this easter egg, the password was successfully updated."
            )
            return new_password

        if not valid_password(new_password):
            print(
                "Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
            )
            continue

        confirm = confirm_new_pass()
        if confirm != new_password:
            print("Passwords do not match. Try again.")
            continue

        update_password(username, new_password)
        apply_hint_update(username)
        print("The password was succesfully updated")
        return new_password
