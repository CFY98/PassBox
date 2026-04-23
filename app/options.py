# EXTERNAL LIBRARIES 
import json
import re
import pwinput

# PASSBOX MODULES
from core.security import (decryption, encryption, derive_app_user)
from core.vault import (vault, edit_vault)
from core.utils import strong_password

# CONTINUE LOGIC
def keep_going(session):
    return input("\nReturn to Main Menu (y/n)? ").strip().casefold() == "y"

# PASSWORD SUGGESTER
def get_password(session):
    suggest_pwd = strong_password(15)
    
    print(f"\nPassword suggestion: {suggest_pwd}")
    if pwinput.pwinput("\nUse suggestion (y/n)? ").strip().casefold() == "y":
        return suggest_pwd
    intended_password = pwinput("Please enter the intended password: ")
    return intended_password

# OPTIONS
def add_entry(session):
    while True:
        domain = input("\nPlease add the name of the site: ")
        domain_name = input("Please enter the username/email: ")
        domain_password = get_password(session)
        
        fzf_id = derive_app_user(domain, session.hmac_key)
        data = vault(session.vault_file)

        if fzf_id in data:
            check = (
                input("This entry already exists. Overwrite (y/n)? ").strip().casefold()
            )
            if check == "n":
                return False

        data.update(
            {
                fzf_id: {
                    "domain": encryption(domain, session.enc_key),
                    "username": encryption(domain_name, session.enc_key),
                    "password": encryption(domain_password, session.enc_key),
                }
            }
        )

        edit_vault(data, session.vault_file)
        
        if keep_going(session):
            break

def view_entries(session):
    while True:
        unlock = vault(session.vault_file)
        if not unlock:
            print("Vault is empty\n")
            break

        for domain, creds in unlock.items():
            print("Site:", decryption(creds["domain"], session.enc_key))
            print("Username:", decryption(creds["username"], session.enc_key))
            print("Password:", decryption(creds["password"], session.enc_key))
            print("-" * 29)

        if keep_going(session):
            break

def update_entry(session):
    while True:
        choice = input("\nPlease enter the name of the entry you want to update: ")
        new_name = input("Please enter the new username/email: ")
        new_password = get_password(session)

        fzf_id = derive_app_user(choice, session.hmac_key)
        entries = vault(session.vault_file)
        
        if fzf_id not in entries:
            print("Entry not found")
            if keep_going(session):
                break
        entries.pop(fzf_id)
        entries.update(
            {
                fzf_id: {
                    "domain": encryption(choice, session.enc_key),
                    "username": encryption(new_name, session.enc_key),
                    "password": encryption(new_password, session.enc_key),
                }
            }
        )

        edit_vault(entries, session.vault_file)
        
        if keep_going(session):
            break

def delete_entry(session):
    while True:
        delete = input("\nPlease enter the name of the entry you want to delete: ")

        fzf_id = derive_app_user(delete, session.hmac_key)
        target = vault(session.vault_file)

        if fzf_id in target:
            target.pop(fzf_id)
            edit_vault(target, session.vault_file)
            print("\nEntry successfully deleted")
        else:
            print("\nEntry not found")
        
        if keep_going(session):
            break

def search_vault(session):
    while True:
        seek_entry = input("\nSearch: ").strip()
        print()
    
        storage = vault(session.vault_file)
        found = False
        
        for key, creds in storage.items():
            domain_key = decryption(creds["domain"], session.enc_key)
        
            if re.search(seek_entry, domain_key, re.IGNORECASE):
                print("---------- RESULTS ----------\n")
                print("Site:", domain_key)
                print("Username:", decryption(creds["username"], session.enc_key))
                print("Password:", decryption(creds["password"], session.enc_key))
                print("-" * 29)
                found = True

        if not found:
            print("Entry not found")

        if keep_going(session):
            break

# FUNCTION MAP
options_map = {
        "1": add_entry,
        "2": view_entries,
        "3": update_entry,
        "4": delete_entry,
        "5": search_vault,
        }
