# EXTERNAL LIBRARIES
import re

# PASSBOX MODULES
from core.security import decryption
from core.utils import (
    build_entry,
    entry_exists,
    get_domain,
    get_id,
    get_user_vault,
    leave,
    user_input,
)
from core.vault import edit_vault, vault


# OPTIONS
def add_entry(session):
    while True:
        domain = get_domain()
        username, password = user_input()
        fzf_id = get_id(domain, session)
        data = get_user_vault(session)

        if entry_exists(fzf_id, data):
            if (
                input("This entry already exists. Overwrite (y/n)? ").strip().casefold()
                == "n"
            ):
                return False

        data.update({fzf_id: build_entry(domain, username, password, session.enc_key)})
        edit_vault(data, session.vault_file)

        if leave():
            break


def view_entries(session):
    while True:
        unlock = vault(session.vault_file)
        if not unlock:
            print("Vault is empty\n")
            break

        for _, creds in unlock.items():
            print("Site:", decryption(creds["domain"], session.enc_key))
            print("Username:", decryption(creds["username"], session.enc_key))
            print("Password:", decryption(creds["password"], session.enc_key))
            print("-" * 29)

        if leave():
            break


def update_entry(session):
    while True:
        domain = get_domain()
        username, password = user_input()
        fzf_id = get_id(domain, session)
        data = get_user_vault(session)

        if not entry_exists(fzf_id, data):
            if input("Entry not found, add to vault (y/n)? ").strip().casefold() == "y":
                data.update(
                    {fzf_id: build_entry(domain, username, password, session.enc_key)}
                )
        if leave():
            break

        data.pop(fzf_id)
        data.update({fzf_id: build_entry(domain, username, password, session.enc_key)})

        edit_vault(data, session.vault_file)

        if leave():
            break


def delete_entry(session):
    while True:
        domain = get_domain()
        fzf_id = get_id(domain, session)
        data = get_user_vault(session)

        if entry_exists(fzf_id, data):
            data.pop(fzf_id)
            edit_vault(data, session.vault_file)
            print("\nEntry successfully deleted")
        else:
            print("\nEntry not found")

        if leave():
            break


def search_vault(session):
    while True:
        seek_entry = input("\nSearch: ").strip()
        print()

        storage = vault(session.vault_file)
        found = False

        for _, creds in storage.items():
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

        if leave():
            break


# FUNCTION MAP
options_map = {
    "1": add_entry,
    "2": view_entries,
    "3": update_entry,
    "4": delete_entry,
    "5": search_vault,
}
