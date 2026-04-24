# EXTERNAL LIBRARIES
import pwinput

from app.main import main

# PASSBOX MODULES
from core.auth import Auth


def load_auth():
    return Auth()


def login_details():
    login_name = input("Please enter your username: ").strip()
    login_password = pwinput.pwinput("Please enter your password: ").strip()
    return (login_name, login_password)


def registration():
    return input("Register (y/n)? ").strip().casefold() == "y"


def register_hint():
    return input("Please enter a memorable hint: ")


# LOGIN DAEMON
def passbox():
    max_attempts = 6
    failures = 0

    auth = load_auth()
    username, password = login_details()

    while failures < max_attempts:
        status, session = auth.login(username, password)

        if status == "invalid_user":
            if not registration():
                return
            hint = register_hint()
            if auth.register(username, password, hint):
                _, session = auth.login(username, password)
                print("\nEntering PassBox...")
                main(session)
            return

        elif status == "invalid_password":
            failures += 1
            attempts_left = max_attempts - failures
            if attempts_left > 0:
                print(f"Please try again. Attempts left: {attempts_left}".upper())
                if failures >= 2:
                    print(auth.get_hint(username))
                if failures >= 4:
                    new_password = auth.change_password(username, password)
                    if new_password != password:
                        password = new_password
            else:
                print("Incorrect password, no attempts left.")
                return
        else:
            print("\nEntering PassBox...")
            main(session)
            return


if __name__ == "__main__":
    passbox()
