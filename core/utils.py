# EXTERNAL IMPORTS
import random
import string

import pwinput


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
