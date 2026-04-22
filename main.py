# PASSBOX MODULES
from options import options_map

# PASSBOX INTERFACE
def passbox(auth):
    menu = {"1": "Add an Entry", "2": "View Entries", "3": "Update Entry", "4": "Delete Entry", "5": "Search", "6": "Log Out"}
    print("What would you like to do?\n")
    for key, value in menu.items():
        print(f"{key}: {value}")
    print()

    prompt = input("Answer: ").strip()
    print()
    try:
        if prompt == "6":
            auth.logout()
            return
        if prompt in options_map:
            options_map[prompt](auth)
    except KeyError:
        print("Please refer to list of options")


