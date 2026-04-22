from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

VAULT = DATA_DIR / "vault.json"
CREDENTIALS = DATA_DIR / "credentials.csv"
KEY = DATA_DIR / "key.key"
