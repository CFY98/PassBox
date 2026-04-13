import pwinput

from auth import Auth
from utils import strong_password, valid_password


def first_hint(password):
    hint = password.count("l")
    print(f"The letter l occurs {hint} times.".capitalize())


def second_hint(password):
    clue = password.find("world")
    print(f"The index of world is {clue}.".capitalize())


def change_password(password):
    while True:
        choice = input("Change password? Yes/No: ").strip().lower()

        if choice == "yes":
            suggestion = strong_password(15)
            print(
                f'Here is a suggestion: {suggestion}\nIf you want to use it, type "use suggestion".\n',
                end="",
            )
            update = pwinput.pwinput("Please enter new password: ")

            if update == "use suggestion":
                update = suggestion
                return update

            confirm = pwinput.pwinput("Please confirm your new password: ")
            if confirm != update:
                print("Passwords do not match. Try again.")
                continue

            if update == password:
                print("Cannot be old password, please try again.")
                continue

            if update == "h3110 w0r1d!!":
                new_password = password.replace("hello world", "h3110 w0r1d!!")
                print(
                    "Thanks for using this easter egg, the password was successfully updated."
                )
                return new_password

            if not valid_password(update):
                print(
                    "Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols."
                )
                continue

            print("The password was succesfully updated")
            return update

        elif choice == "no":
            print("No worries~")
            return password

        else:
            retry = input("Did I catch that right? Yes/No: ").strip().lower()
            if retry == "yes":
                return password
            elif retry != "no":
                print('It\'s a "yes" or "no" answer.')
            else:
                continue


def main():
    max_attempts = 6
    failures = 0

    while failures < max_attempts:
        auth = Auth()
        username = input("Please enter your username: ").strip()
        password = pwinput.pwinput("Please enter your password: ").strip()
        login = auth.login(username, password)

        if login == "Username not found":
            register = input("Username not found. Would you like to register? (y/n): ")
            if register.lower() == "y":
                return auth.register(username, password)
            else:
                continue

        elif login == "Incorrect password, please try again":
            failures += 1
            attempts_left = max_attempts - failures
            if attempts_left > 0:
                print(f"Please try again. Attempts left: {attempts_left}".upper())
                if failures == 2:
                    first_hint(password)
                elif failures == 3:
                    second_hint(password)
                if failures >= 3:
                    new_password = change_password(password)
                    if new_password != password:
                        password = new_password
            else:
                print("Incorrect password, no attempts left.")
                break
        else:
            return login


if __name__ == "__main__":
    main()
