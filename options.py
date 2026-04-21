import json
import re

from utils import decryption, encryption, hash_domain, vault


def edit_vault(value):
    with open("vault.json", "w") as f:
        json.dump(value, f, indent=4)


def add_entry():
    domain = input("Please add the name of the site: ")
    domain_name = input("Please enter the username/email: ")
    domain_password = input("Please enter the password: ")

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
            hash_key: {
                "username": encryption(domain_name),
                "password": encryption(domain_password),
            }
        }
    )

    edit_vault(data)


def view_entries():
    unlock = vault()

    for domain, creds in unlock.items():
        print("Site:", domain)
        print("Username:", decryption(creds["username"]))
        print("Password:", decryption(creds["password"]))
        print("-" * 20)


def update_entry():
    choice = input("Please enter the name of the entry you want to update: ")
    new_name = input("Please enter the new username/email: ")
    new_password = input("Please enter the new password: ")

    entries = vault()

    entries.update(
        {
            hash_domain(choice): {
                "username": encryption(new_name),
                "password": encryption(new_password),
            }
        }
    )

    edit_vault(entries)


def delete_entry():
    delete = input("Please enter the name of the entry you want to delete: ")

    target = vault()

    hash_delete = hash_domain(delete)

    if hash_delete in target:
        target.pop(hash_delete)
        edit_vault(target)
    else:
        print("Entry not found")


def search_vault():
    seek_entry = input("Please type the name of the entry here: ")
    
    storage = vault()
    
    pattern = re.compile(seek_entry,re.IGNORECASE)
    
    for key, creds in storage.items():
        domain = decryption(key)
        
        if seek_entry in domain:
            print("Found:")
            print("Site:", domain)
            print("Username:", decryption(creds["username"]))
            print("Password:", decryption(creds["password"]))
            return

    print("Entry not found")

options_map = {
        "add entry": add_entry,
        "view entries": view_entries,
        "update entry": update_entry,
        "delete entry": delete_entry,
        "search": search_vault,
        }
