# EXTTERNAL LIBRARIES
from pathlib import Path

# ESTABLISH PROJECT ROOT & DATA DIR
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

# DATA FILES PATHS
VAULT = DATA_DIR / "vault.json"
CREDENTIALS = DATA_DIR / "credentials.csv"
KEY = DATA_DIR / "key.key"
