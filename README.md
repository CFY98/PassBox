# 🔐 PassBox

PassBox is a CLI password manager with a hybrid secruity model to explore how secure system design and cryptographic separation of concerns. It features a hybrid model where authentication, session state, and encryption responisibilities are strictly separated.

## 🧠 Features

- Per-user encrypted vaults with unique vault files
- Argon2id key derivation for master password
- HMAC-based stable entry IDs for lookup, update, and removal
- Symmetric authenticated encryption (Fernet) for vault data and app_username
- Decryption only occurs at display time
- Fuzzy search on hashed domain name values
- CLI-based interface

## 💡 Security Model
```
                 ENTROPY LAYER

                  os.urandom()
                       |
         user_salt (Randomised per user)
    app_salt (global system salt, generated once)

----------------------------------------------------

                    ID LAYER

              username + app_salt
                       │
                       │ HMAC-SHA256
                       │
          username_hmac (stable user ID)

----------------------------------------------------

              KEY DERIVATION LAYER
                 master_password
                       │   
                       │ Argon2id (KDF)
                       │
                   master_key
                       │   
                       │ SHA256 key derivation
                       │
                       ├── enc_key → base64(Fernet-compatible key)
                       └── hmac_key → SHA256-derived signing key
```
- **Vault entries**: domain names, usernames and passwords are encrypted with Fernet
- **Credentials**: usernames encrypted with Fernet, passwords stord as Argon2id hashes for verification, hints as plain text (non-sensitive metadata)
- **Vault Entry IDs**: domain names hashed with HMAC-SHA256 for stable lookup without exposing raw values
- **Per-user vaults**: each user has an isolated vault file which is encrypted with a key to their master password

## Session Model

PassBox uses a runtime session-based design:
- `Auth` validates credentials and creates a `Session`
- `Session` derives and stores cryptographic kesy
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
│   ├── main.py          # Session lifecycle 
│   ├── options.py       # User session and derived keys
│   └── session.py       # Runtime session object with lazy load methods
├── core/
│   ├── auth.py          # Login, user registration, and hint logic
│   ├── security.py      # Encryption, salt generation, hashing, and key derivation
│   ├── utils.py         # Password suggestion and validation logic
│   └── vault.py         # Vault load and save logic
├── lib/
│   └── config.py.       # Path configuration
├── data/                # Runtime data (ignored by git)
│   ├── credentials.csv    
│   ├── app.salt
│   └── vaults/
├── requirements.txt     # Non-built-in Python libraries
├── README               # This file
└── LICENSE              # MIT License
```
> **Note:** The `data` directory is excluded from version control. It is automatically created on first run.

## 📜 License

This project is licensed under the **MIT license**.
