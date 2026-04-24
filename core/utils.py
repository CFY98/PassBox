# EXTERNAL IMPORTS
import random
import string

import pwinput

# PASSBOX MODULES
from core.security import derive_app_user, encryption
from core.vault import vault


# OPTIONS MENU UTILITIES
def leave():
    return input("\nReturn to Main Menu (y/n)? ").strip().casefold() == "y"


def user_input():
    domain_user = input("Please enter the username/email: ")
    domain_password = get_password()
    return (domain_user, domain_password)


def get_domain():
    return input("\nPlease enter the name of the site: ")


def get_id(domain, session):
    return derive_app_user(domain, session.hmac_key)


def get_user_vault(session):
    return vault(session.vault_file)


def entry_exists(fzf_id, data):
    return fzf_id in data


def build_entry(domain, username, password, enc_key):
    return {
        "domain": encryption(domain, enc_key),
        "username": encryption(username, enc_key),
        "password": encryption(password, enc_key),
    }


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
    intended_password = pwinput.pwinput("Please enter the intended password: ")
    return intended_password
