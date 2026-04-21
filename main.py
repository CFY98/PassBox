# PASSBOX MODULES
from options import options_map

def interface():
    menu = ["Add an Entry", "View Entries", "Update Entry", "Delete Entry", "Search"]
    print("What would you like to do?\n")
    print("\n".join(menu))
    print()

    prompt = input("Answer: ").strip().casefold()
    try:
        if prompt in options_map:
            options_map[prompt]()
    except KeyError:
        print("Please refer to list of options")
