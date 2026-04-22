# PASSBOX MODULES
from options import options_map

# PASSBOX INTERFACE
def menu():
    menu = {"1": "Add an Entry", "2": "View Entries", "3": "Update Entry", "4": "Delete Entry", "5": "Search", "6": "Log Out"}
    print("\n---------- MAIN MENU ----------\n")
    for key, value in menu.items():
        print(f"{key}: {value}")
    print()

def passbox(auth):
    while True:
        menu()
        prompt = input("Answer: ").strip()
        print()
        try:
            if prompt == "6":
                auth.logout()
                break
            if prompt in options_map:
                options_map[prompt](auth)
        except KeyError:
            print("Please refer to list of options")


