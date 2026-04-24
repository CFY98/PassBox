# PASSBOX MODULES
from .options import options_map

# PASSBOX INTERFACE
def menu():
    menu = {"1": "Add an Entry", "2": "View Entries", "3": "Update Entry", "4": "Delete Entry", "5": "Search", "6": "Log Out"}
    print("\n-------- MAIN MENU --------\n")
    for key, value in menu.items():
        print(f"{key}: {value}")

def main(session):
    while True:
        menu()
        prompt = input("\nAnswer: ").strip()
        print()
        try:
            if prompt == "6":
                print("Exiting PassBox...\n")
                return
            options_map[prompt](session)
        except KeyError:
            print("\nPlease refer to list of options")

if __name__ == "__main__":
    print("Module not meant to be run directly")
