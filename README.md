# 🔐 PassBox

PassBox is a CLI password manager with a hybrid security model to explore how secure system design and cryptographic separation of concerns. It features a hybrid model where authentication, session state, and encryption responisibilities are strictly separated.

## 🧠 Features

- **Hybrid Encryption Model** — Authentication, session state, and vault access strictly separated with symmetric Fernet encryption for vault data and credentials.
- **Key Derivation** — Argon2id KDF for master password hashing with SHA256-derived encryption and HMAC signing keys.
- **Stable Entry IDs** — HMAC-SHA256 hashed domain names for consistent lookup, update, and removal without exposing raw values.
- **Deferred Decryption** — Vault data decrypted only at display time to minimise memory exposure.
- **Pattern Search** — Fzf-inspired regex search across decrypted entry names for fast vault querying.
- **CLI Interface** — Session-based design with strict separation between auth, session, and vault layers.

## 💡 Security Model
```
ENTROPY LAYER

os.urandom() -> user_salt (randomised per user), app_salt(global system salt)

----------------------------------------------------

ID LAYER

username + app_salt -> HMAC-SHA256 -> username_hmac (stable user ID)

----------------------------------------------------

KEY DERIVATION LAYER

master_password -> Argon2id (KDF) -> master_key -> SHA256 key derivation -> 
[enc_key -> base64(Fernet-compatible key)], [hmac_key -> SHA256-derived signing key]

```
- **Vault entries**: domain names, usernames and passwords are encrypted with Fernet
- **Credentials**: usernames encrypted with Fernet, passwords stord as Argon2id hashes for verification, hints as plain text (non-sensitive metadata)
- **Vault Entry IDs**: domain names hashed with HMAC-SHA256 for stable lookup without exposing raw values
- **Per-user vaults**: each user has an isolated vault file which is encrypted with a key to their master password

## 🪪 Session Model

PassBox uses a runtime session-based design:
- `Auth` validates credentials and creates a `Session`
- `Session` derives and stores cryptographic keys
- `main.py` operates on active user session

## 🛠️ Technologies

- **Python**: Main programming language
- **argon2-cffi**: Argon2id password hashing and key derivation
- **hmac / hashlib (built-in)**: HMAC-SHA256 for stable entry IDs
- **cryptography (Fernet)**: symmetric encryption
- **json**: encrypted data storage
- **csv**: credential storage

## 🚀 Getting Started

📌 Requirements

- Python 3.10+ installed on your system

📦 How to Run

1. Clone the repository:

```
git clone https://github.com/CFY98/PassBox.git
```

2. Navigate to the project folder:

```
cd PassBox
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run PassBox:

```
python passbox.py
```

- The script will perform its encryption routine with user input as defined in the code.
- For the unit tests to work, there must be at least 1 user account. Please see the recommended account when conducting tests.
```
Recommended app username: test
Recommended app password: test
Recommended domain name: test.com
```
##  ⚠️ Disclaimer

> PassBox is a learning project designed to explore cryptographic concepts and secure system design. It is **not** intended for production use or as a replacement for established password managers.

## 🕛 Future Improvements

- Session locking after repeated failures
- Flask implementation
- Audit logging for security-relevant events
- Clipboard copy for passwords

## 🗂 Project Structure

```
PassBox/
├── passbox.py           # Login entry point
├── app/
│   ├── main.py          # Session lifecycle 
│   ├── options.py       # User session and derived keys
│   └── session.py       # Runtime session object with lazy load methods
├── core/
│   ├── auth.py          # Login, user registration, and hint logic
│   ├── security.py      # Encryption, salt generation, hashing, and key derivation
│   ├── utils.py         # Password suggestion and validation logic
│   └── vault.py         # Vault load and save logic
├── lib/
│   └── config.py        # Path configuration
├── tests/               # Unit tests for app and core modules
│   ├── test_auth.py    
│   ├── test_main.py
│   ├── test_options.py 
│   ├── test_passbox.py
│   ├── test_session.py 
│   ├── test_utils.py
│   └── test_vault.py   
├── data/                # Runtime data (ignored by git)
│   ├── credentials.csv    
│   ├── app.salt
│   └── vaults/
├── requirements.txt     # Non-built-in Python libraries
├── README.md            # This file
└── LICENSE              # MIT License
```
> **Note:** The `data` directory is excluded from version control. It is automatically created on first run.

## 📜 License

This project is licensed under the **MIT license**.
