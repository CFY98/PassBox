import string
import pwinput

def first_hint(password):
    hint = password.count("l")
    print(f"The letter l occurs {hint} times.".capitalize())

def second_hint(password):
    clue = password.find("world")
    print(f"The index of world is {clue}.".capitalize())
    
def change_password(password):
    while True:
        choice = input("Change password? Yes/No: ").strip().lower()
    
        if choice == 'yes':
            suggestion = strong_password(15)
            print(f"Here is a suggestion: {suggestion}\nIf you want to use it, type \"use suggestion\".\n", end="")
            update = pwinput.pwinput("Please enter new password: ")

            if update == 'use suggestion':
                update = suggestion
                return update
            
            confirm = pwinput.pwinput("Please confirm your new password: ")
            if confirm != update:
                print("Passwords do not match. Try again.")
                continue
            
            if update == password:
                print("Cannot be old password, please try again.")
                continue

            if update == 'h3110 w0r1d!!':
                    new_password = password.replace("hello world","h3110 w0r1d!!")
                    print("Thanks for using this easter egg, the password was successfully updated.")
                    return new_password
            
            if not valid_password(update):
                print("Password must be between 5-15 characters long, with a minimum of 2 letters, numbers and symbols.")
                continue
            
            print("The password was succesfully updated")
            return update
            
        elif choice == 'no':
            print("No worries~")
            return password
    
        else:
            retry = input("Did I catch that right? Yes/No: ").strip().lower()
            if retry == 'yes':
                return password
            elif retry != 'no':
                print("It's a \"yes\" or \"no\" answer.")
            else:
                continue

def encryption(password):
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher = Fernet(key)

    enc_password = cipher.encrypt(password.encode("utf-8"))
    dec_password = cipher.decrypt(enc_password).decode("utf-8")

    return f"Encryption: {enc_password}\nDecryption: {dec_password}"

def valid_password(password):
    numbers = sum(c.isnumeric() for c in password) 
    letters = sum(c.isalpha() for c in password)
    symbols = sum(c in string.punctuation for c in password)

    return numbers >=2 and letters >=2 and symbols >= 2 and (5 <= len(password) <=15)

def strong_password(length=15):
    import random
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

    return ''.join(characters)

def main():
    password = "hello world"
    max_attempts = 6
    failures = 0

    while failures < max_attempts:
        x = pwinput.pwinput("Please enter your password: ")
        
        if x == password:
            print("That is the correct password.")
            print(encryption(password))
            if password == "h3110 w0r1d!!":
                print("Hello to you too ;)")
                break
            break
        else:
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

    
if __name__ == "__main__":
    main()