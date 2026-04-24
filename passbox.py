# EXTERNAL LIBRARIES
import pwinput

from app.main import main

# PASSBOX MODULES
from core.auth import Auth


# LOGIN HELPERS
def load_auth():
    return Auth()


def login_name():
    return input("\nPlease enter your username: ").strip()


def login_password():
    return pwinput.pwinput("Please enter your password: ").strip()


def registration():
    return input("\nRegister (y/n)? ").strip().casefold() == "y"


def register_hint():
    return input("\nPlease enter a memorable hint: ")


# LOGIN DAEMON
def passbox():
    auth = load_auth()

    while True:
        max_attempts = 4
        failures = 0

        username = login_name()
        while failures < max_attempts:
            password = login_password()
            status, session = auth.login(username, password)

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
                    print("\nIncorrect password, no attempts left.")
                    return

                print(f"\nPlease try again. Attempts left: {attempts_left}".upper())

                if failures >= 1:
                    print("\nHint:", auth.get_hint(username))

                if failures >= 2:
                    new_password = auth.update_cache_pass(username, password)
                    if new_password:
                        password = new_password
                    continue

            else:
                main(session)
                return


if __name__ == "__main__":
    passbox()
