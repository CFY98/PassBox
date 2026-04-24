# EXTERNAL LIBRARIES
import pwinput

from app.main import main

# PASSBOX MODULES
from core.auth import Auth
from core.utils import change_password


# LOGIN HELPERS
def load_auth():
    return Auth()


def login_name():
    return input("Please enter your username: ").strip()


def login_password():
    return pwinput.pwinput("Please enter your password: ").strip()


def registration():
    return input("Register (y/n)? ").strip().casefold() == "y"


def register_hint():
    return input("Please enter a memorable hint: ")


# LOGIN DAEMON
def passbox():
    auth = load_auth()

    while True:
        max_attempts = 6
        failures = 0

        username = login_name()

        while failures < max_attempts:
            password = login_password()
            status, session = auth.login(username, password)

            if status == "valid":
                main(session)
                return

            if status == "invalid_user":
                if not registration():
                    break

                hint = register_hint()
                if auth.register(username, password, hint):
                    _, session = auth.login(username, password)
                    main(session)
                return

            elif status == "invalid_password":
                failures += 1
                attempts_left = max_attempts - failures

                if attempts_left == 0:
                    print("Incorrect password, no attempts left.")
                    return

                print(f"Please try again. Attempts left: {attempts_left}".upper())

                if failures >= 2:
                    print(auth.get_hint(username))

                if failures >= 4:
                    new_password = change_password(username, password)
                    if not new_password:
                        return password

            else:
                main(session)
                return


if __name__ == "__passbox__":
    passbox()
