# EXTERNAL IMPORTS
import json
import re

# PASSWORD SUGGESTER
def get_password(auth):
    if auth is None:
        raise ValueError("Auth required for password generation")

    suggest_pwd = auth.strong_password(15)
    
    print(f"Suggestion: {suggest_pwd}")
    use = input("Use suggestion (Yes/No)? ").strip().casefold()
    if use == "yes":
        return suggest_pwd
    intended_password = input("Please enter the intended password: ")
    return intended_password

# PASSBOX IMPORTS
from utils import decryption, encryption, vault, hash_domain

# JSON WRITER
def json_edit(value):
    with open("VAULT", "w") as f:
        json.dump(value, f, indent=4)

# OPTIONS
def add_entry(auth=None):
    domain = input("Please add the name of the site: ")
    domain_name = input("Please enter the username/email: ")
    domain_password = get_password(auth)

    hash_key = hash_domain(domain)

    data = vault()
    if hash_key in data:
        check = (
            input("This entry already exists. Overwrite (Yes/No)? ").strip().casefold()
        )
        if check == "no":
            return False

    data.update(
        {
            hash_domain(domain): {
                "domain": encryption(domain),
                "username": encryption(domain_name),
                "password": encryption(domain_password),
            }
        }
    )

    json_edit(data)


def view_entries(auth=None):
    unlock = vault()
    if not unlock:
        print("Vault is empty\n")

    for domain, creds in unlock.items():
        print("Site:", decryption(creds["domain"]))
        print("Username:", decryption(creds["username"]))
        print("Password:", decryption(creds["password"]))
        print("-" * 20)


def update_entry(auth=None):
    choice = input("Please enter the name of the entry you want to update: ")
    new_name = input("Please enter the new username/email: ")
    new_password = get_password(auth)

    hash_choice = hash_domain(choice)
    entries = vault()
    
    entries.pop(hash_choice)
    entries.update(
        {
            hash_choice: {
                "domain": encryption(choice),
                "username": encryption(new_name),
                "password": encryption(new_password),
            }
        }
    )

    json_edit(entries)


def delete_entry(auth=None):
    delete = input("Please enter the name of the entry you want to delete: ")

    target = vault()

    hash_delete = hash_domain(delete)

    if hash_delete in target:
        target.pop(hash_delete)
        json_edit(target)
    else:
        print("Entry not found")


def search_vault(auth=None):
    seek_entry = input("Search: ")
    print()
    
    storage = vault()
    
    for key, creds in storage.items():
        domain_key = decryption(creds["domain"])
        
        if re.search(seek_entry, domain_key, re.IGNORECASE):
            print("Found:\n")
            print("Site:", domain_key)
            print("Username:", decryption(creds["username"]))
            print("Password:", decryption(creds["password"]))
            print("-" * 20)
            return

    print("Entry not found")

# FUNCTION MAP
options_map = {
        "1": add_entry,
        "2": view_entries,
        "3": update_entry,
        "4": delete_entry,
        "5": search_vault,
        }
