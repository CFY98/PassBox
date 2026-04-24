# EXTERNAL LIBRARIES
from pathlib import Path

# ESTABLISH PROJECT ROOT & DATA DIR
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# VAULT DIRECTORY PATH
VAULT_DIR = DATA_DIR / "vaults"
VAULT_DIR.mkdir(exist_ok=True)

# DATA FILE PATHS
CREDENTIALS = DATA_DIR / "credentials.csv"
APP_SALT = DATA_DIR / "app.salt"
