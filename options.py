# EXTERNAL IMPORTS
import json
import re

# PASSBOX IMPORTS
from config import VAULT
from security import decryption, encryption, hash_domain
from vault import vault

# CONTINUE LOGIC
def keep_going(auth=None):
    return input("\nReturn to Main Menu (Yes/No)? ").strip().casefold() == "yes"

# PASSWORD SUGGESTER
def get_password(auth):
    if auth is None:
        raise ValueError("Auth required for password generation")

    suggest_pwd = auth.strong_password(15)
    
    print(f"\nPassword suggestion: {suggest_pwd}")
    use = input("\nUse suggestion (Yes/No)? ").strip().casefold()
    if use == "yes":
        return suggest_pwd
    intended_password = input("Please enter the intended password: ")
    return intended_password

# JSON WRITER
def json_edit(value):
    with open(VAULT, "w") as f:
        json.dump(value, f, indent=4)

# OPTIONS
def add_entry(auth=None, vault_key=None):
    while True:
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
                hash_key: {
                    "domain": encryption(domain, vault_key),
                    "username": encryption(domain_name, vault_key),
                    "password": encryption(domain_password, vault_key),
                }
            }
        )

        json_edit(data)
        
        if keep_going(auth):
            break

def view_entries(auth=None, vault_key=None):
    while True:
        unlock = vault()
        if not unlock:
            print("Vault is empty\n")
            break

        for domain, creds in unlock.items():
            print("Site:", decryption(creds["domain"], vault_key))
            print("Username:", decryption(creds["username"], vault_key))
            print("Password:", decryption(creds["password"], vault_key))
            print("-" * 29)

        if keep_going(auth):
            break

def update_entry(auth=None, vault_key=None):
    while True:
        choice = input("Please enter the name of the entry you want to update: ")
        new_name = input("Please enter the new username/email: ")
        new_password = get_password(auth)

        hash_choice = hash_domain(choice)
        entries = vault()
        
        if hash_choice not in entries:
            print("Entry not found")
            if keep_going(auth):
                break
        entries.pop(hash_choice)
        entries.update(
            {
                hash_choice: {
                    "domain": encryption(choice, vault_key),
                    "username": encryption(new_name, vault_key),
                    "password": encryption(new_password, vault_key),
                }
            }
        )

        json_edit(entries)
        
        if keep_going(auth):
            break

def delete_entry(auth=None, vault_key=None):
    while True:
        delete = input("Please enter the name of the entry you want to delete: ")

        target = vault()

        hash_delete = hash_domain(delete)

        if hash_delete in target:
            target.pop(hash_delete)
            json_edit(target)
            print("Entry successfully deleted")
        else:
            print("Entry not found")
        
        if keep_going(auth):
            break

def search_vault(auth=None, vault_key=None):
    while True:
        seek_entry = input("Search: ").strip()
        print()
    
        storage = vault()
        found = False
        
        for key, creds in storage.items():
            domain_key = decryption(creds["domain"], vault_key)
        
            if re.search(seek_entry, domain_key, re.IGNORECASE):
                print("---------- RESULTS ----------\n")
                print("Site:", domain_key)
                print("Username:", decryption(creds["username"], vault_key))
                print("Password:", decryption(creds["password"], vault_key))
                print("-" * 29)
                found = True

        if not found:
            print("Entry not found")

        if keep_going(auth):
            break

# FUNCTION MAP
options_map = {
        "1": add_entry,
        "2": view_entries,
        "3": update_entry,
        "4": delete_entry,
        "5": search_vault,
        }
