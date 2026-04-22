# EXTERNAL IMPORTS
import pwinput

# PASSBOX MODULES
from auth import Auth
from main import main   

# LOGIN DAEMON
def passbox():
    max_attempts = 6
    failures = 0

    auth = Auth()
    username = input("Please enter your username: ").strip()

    while failures < max_attempts:
        password = pwinput.pwinput("Please enter your password: ").strip()
        status, vault_key = auth.login(username, password)

        if status == "User not found":
            register = input(
                "User not found. Would you like to register (y/n)? "
            ).strip().casefold()
            if register == "y":
                hint = input("Please enter a memorable hint: ")
                if auth.register(username, password, hint):
                    login = auth.login(username, password)
                    main(auth, vault_key)
            return

        elif status == "Incorrect password, please try again":
            failures += 1
            attempts_left = max_attempts - failures
            if attempts_left > 0:
                print(f"Please try again. Attempts left: {attempts_left}".upper())
                if failures >= 2:
                    hint_key = auth.derive_creds(password)
                    print(auth.get_hint(username, hint_key))
                if failures >= 4:
                    new_password = auth.change_password(username, password)
                    if new_password != password:
                        password = new_password
            else:
                print("Incorrect password, no attempts left.")
                return
        else:
            main(auth, vault_key)
            return

if __name__ == "__main__":
    passbox()
