import random
import string

import pandas as pd


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


def update_password(username, update):
    df = pd.read_csv("credentials.csv")
    df.loc[df["username"] == username, "password"] = update
    df.to_csv("credentials.csv", index=False)
