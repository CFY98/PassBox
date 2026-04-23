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
APP_SALT_PATH = DATA_DIR / "app.salt"

def get_app_salt():
    return APP_SALT_PATH.read_bytes()

APP_SALT = get_app_salt()

HMAC_USER = DATA_DIR / "hmac_user.key"
