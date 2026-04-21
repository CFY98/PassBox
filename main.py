import csv

import pwinput

from auth import Auth


def get_hint(username):
    with open("credentials.csv", "r") as f:
        hint = csv.DictReader(f)
        for row in hint:
            if row["username"] == username:
                return f"Hint: {(row['hint'].strip())}"


def main():
    max_attempts = 5
    failures = 0

    username = input("Please enter your username: ").strip()
    while failures < max_attempts:
        auth = Auth()
        password = pwinput.pwinput("Please enter your password: ").strip()
        login = auth.login(username, password)

        if login == "Login details not found":
            register = input(
                "Login details not found. Would you like to register? (y/n): "
            )
            if register.lower() == "y":
                hint = input("Please enter a memorable hint: ")
                return auth.register(username, password, hint)
            else:
                break

        elif login == "Incorrect password, please try again":
            failures += 1
            attempts_left = max_attempts - failures
            if attempts_left > 0:
                print(f"Please try again. Attempts left: {attempts_left}".upper())
                if 2 <= failures:
                    print(get_hint(username))
                if failures >= 4:
                    new_password = auth.change_password(username, password)
                    if new_password != password:
                        password = new_password
            else:
                print("Incorrect password, no attempts left.")
                break
        else:
            return login


if __name__ == "__main__":
    main()
