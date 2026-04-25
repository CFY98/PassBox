# EXTERNAL LIBRARIES
import json
from pathlib import Path


# VAULT FUNCTIONS
def edit_vault(value, vault_file):
    with open(vault_file, "w") as f:
        json.dump(value, f, indent=4)


def vault(vault_file):
    path = Path(vault_file)
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}
