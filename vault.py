# EXTERNAL LIBRARIES
import json

# PASSBOX MODULES
from config import VAULT

# VAULT FUNCTIONS
def new_vault():
    VAULT.write_text(json.dumps({}), encoding="utf-8")


def vault():
    if VAULT.exists():
        try:
            with VAULT.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    else:
        new_vault()
        return {}

