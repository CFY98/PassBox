# EXTERNAL LIBRARIES 
import pwinput

# PASSBOX MODULES
from core.auth import Auth
from app.main import main   

# LOGIN DAEMON
def passbox():
    max_attempts = 6
    failures = 0

    auth = Auth()
    username = input("Please enter your username: ").strip()

    while failures < max_attempts:
        password = pwinput.pwinput("Please enter your password: ").strip()
        status, session = auth.login(username, password)

        if status == "invalid_user":
            if input("Register (y/n)? ").strip().casefold() == "y":
                hint = input("Please enter a memorable hint: ")
                if auth.register(username, password, hint):
                    status, session = auth.login(username, password)
                    print("Loading Vault --->")
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
            print("Loading Vault --->")
            main(session)
            return

if __name__ == "__main__":
    passbox()
