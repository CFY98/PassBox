# 🔐 PassBox

PassBox is a CLI password manager with a hybrid secruity model to explore how secure systems work. It separates data identification (via HMAC hashing) from data protection (via encryption), and derives all keys from the user's master password.

## 🧠 Features

- Per-user encrypted vaults with unique vault files
- Argon2id key derivation for vault and credential encryption
- HMAC-based stable entry IDs for lookup, update, and removal
- Fernet encryption to protect all sensitive data
- Decryption only occurs at display time
- Fuzzy search on decrypted domain values
- CLI-based interface

## 💡 Security Model

```
master_password -> Argon2id -> vault_key -> Fernet -> encrypted vault entries
master_password -> Argon2id -> creds_key -> Fernet -> encrypted credentials
vault_key -> SHA256 -> hmac_key -> HMAC -> stable entry IDs
```
- **Vault entries**: domain names, usernames and passwords are encrypted with Fernet
- **Credentials**: usernames encrypted with Fernet, passwords hashed with Argon2id, hints as plain text
- **Entry IDs**: domain names hashed with HMAC-SHA256 for stable lookup without exposing plain text
- **Per-user vaults**: each user has an isolated vault file which is encrypted with a key to their master password

## 🛠️ Technologies

- **Python**: Main programming language
- **argon2-cffi**: Argon2id password hashing and key derivation
- **hmac + hashlib (built-in)**: HMAC-SHA256 for stable entry IDs
- **cryptography**: Fernet symmetric encryption
- **json**: encrypted data storage
- **csv**: credential storage
- **pandas**: credential updates

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

🔹 The script will perform its encryption routine with user input as defined in the code.

##  ⚠️ Disclaimer

> PassBox is a learning project designed to explore cryptographic concepts and secure system design. It is **not** intended for production use or as a replacement for established password managers.

## ⏱️ Future Improvements

- Session locking after repeated failures
- Flask implementation
- Audit logging for security-relevant events
- Clipboard copy for passwords

## 🗂 Project Structure

```
PassBox/
├── passbox.py           # Login entry point
├── app/
│   ├── main.py          # Menu logic
│   ├── options.py       # User session and derived keys
│   └── session.py       # Interface options and function map
├── core/
│   ├── auth.py          # Login, registration, password, and hint logic
│   ├── security.py      # Encryption, hashing, key derivation
│   └── vault.py         # Vault load and save logic
├── lib/
│   └── config.py.       # Path configuration
├── data/                # Runtime data (excluded from version control)
│   ├── credentials.csv    
│   ├── creds.salt
│   ├── hmac_user.key
│   └── vaults/
├── requirements.txt     # Non-built-in Python libraries
├── README               # This file
└── LICENSE              # MIT License
```
> **Note:** The `data` directory is excluded from version control. It is automatically created on first run.

## 📜 License

This project is licensed under the **MIT license**.
