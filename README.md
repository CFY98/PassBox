# 🔎 Note
This project was submitted as the final project for CS50’s Introduction to Programming with Python. The project structure was designed in accordance to the course criteria.

Additionally, the documentation is intentionally detailed and verbose to clearly explain design decisions, security rationale, and implementation trade-offs as part of the learning process.

# 🔐 PassBox

PassBox is a CLI password manager designed to explore how secure system design and cryptographic separation of concerns. It features a hybrid model where authentication, session state, and encryption responsibilities are strictly separated.

## 🧠 Features

1) Per-user encrypted vaults with unique vault files
> In its initial stages, this project only had one user account which was generated via the register module in the Auth class. I would later discover that this would become a potential security issue since it would mean other users could access the same account and sensitive data. Therefore, I decided to move into a model that allowed for more than one user, with each vault being access by the master key which is derived from the user account salts.
2) Argon2id key derivation for master password
> When designing this project, I was thinking of ways to ensure the app password for each user would be protected securely in a separate manner from the app username so if the username were somehow decrypted from an attacker, the password would be hashed. I considered PBKDF2 but decided to go with Argon2id due to its advanced memory hardness, optimised resistance against GPU-based cracking attacks, side-channel attack resistance, and use of salts. User salts are created at via os.urandom so even if users shared the same app passwords, each user has a unique salt linked to their account. This alongside their app password is processed through Argon2id to derive a unique master key to access sensitive data.
3) HMAC-based stable entry IDs for lookup, update, and removal
> As part of the sub-menu, I was keen on implementing a search feature to help with lookups should a user have more than say, 10, entries. However because the sensitive data in the vault is encrypted via Fernet which produces a different ciphertext each time. Therefore encrypted values can no longer be compared or indexed directly. To maintain the privacy of sensitive data while enabling deterministic lookup, I implemented parallel hashing via HMAC-SHA256 for entry names. These are stored as hex which allows them to carry a fixed, deterministic representation to allow consistent comparisons without exposing the original data.
4) Symmetric authenticated encryption (Fernet) for vault data and app_username
> Personally, I am quite concerned about privacy and was a bit horrified to learn that usernames are typically stored as plain text for user accounts in enterprise password managers. Although I learned usernames are typically treated as non-sensitive identifiers, this project encrypts them to reduce metadata exposure in the event of local file compromise, particularly where usernames may contain personal information such as email addresses. The concerns here were not simply for this application, but how users interact with services in general should a user use the same username across multiple accounts. Therefore, I decided to implement Fernet to randomise encryption of the app username a user inputs. However, this did introduce an obstacle for the programme to connect what the user typed to the data stored in the credentials.csv during verfication at login. Therefore, app usernames are also hashed via HMAC-SHA256 to allow for deterministic lookups so the programme can match the app username inputted by the user with the hashed value stored in the credentials file.
5) Decryption only occurs at display time
> The master key is derived from the app password and the user_salt via Argon2id. This master-key then provides two keys, one hmac_key for hashed values and the enc_key for decryption of sensitive data once in the session. These are lazy loaded via the Session class to help conserve on memory usuage to only call them when they are needed, rather than passing them around the programme during the whole session. When a user adds an entry to the vault, it's immediately encrypted via Fernet to a json files which is based on the hased app username of the user. This is to help protect sensitive data from attackers should they have access to the system the json files are stored in. This helps provide a layer of security during data at rest.
6) Fuzzy-inspired search on decrypted domain name values
> As mentioned in section 3, entry names in the vault are stored as two separate values, hashed via HMAC-SHA256 and encrypted via Fernet. When designing the search feature, an issue I contemplated the user may run into is the possibility of forgetting or being unsure of the name of the entry. Inspired by the fzf command line tool in terminals, I wanted to see if I could incorporate something similar to this feature into this programme. I did this by implementing the re library where the user input is passed as a pattern and searched against the decrypted entry name. This would provide, if it exists, the entry name even if the user didn't type the full name, say go for google, etc.
6) CLI-based interface
> I initially had the intention of implementing Flask for this final project but the project had expanded beyond my initial scope of a single-user access to the vault. Learning about the different cryptography methods alongside refactoring the code along the way, I felt the project had become quite robust relative to the knowledge I gained during the CS50 Python Course. At this stage, I concluded there were still concepts I needed to digest, such as key derivation, before adding new features. Therefore, I decided to use a CLI-based interface with a solid foundation for future expansion beyond the scope of the course.

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
1) **Vault entries**: entry names, usernames, and passwords are encrypted with Fernet and decrypted during a user session via the enc_key provided by the master-key which is derived from the user-salt.
2) **Credentials**: app usernames encrypted with Fernet, app passwords stored as Argon2id hashes for verification, app hints as plain text (non-sensitive metadata).
3) **Stable IDs**: entry names and app usernames are also hashed with HMAC-SHA256 for stable lookup without exposing raw values. The app username is derived from the app salt while the entry names inside the Vault are derived from a hmac_key provided by the master-key.
4) **Per-user vaults**: each user has an isolated vault file which is encrypted with a key to their master password.

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

1. Navigate to the project folder:

```
cd project
```

2. Install dependencies:

```
pip install -r requirements.txt
```

4. Run PassBox:

```
python project.py
```

- The script will perform its encryption routine with user input as defined in the code.
- For the unit tests to work, there must be at least 1 user account. Please see the recommended account when conducting tests.
> Recommended app username: test
> Recommended app password: test
> Recommended entry name: test.com

## ⚠️ Disclaimer

> PassBox is a learning project designed to explore cryptographic concepts and secure system design. It is **not** intended for production use or as a replacement for established password managers.

## 🗂 Project Structure

```
PassBox/
├── project.py           # Login entry point
├── passbox.py           # Session lifecycle
├── options.py           # User session and derived keys
├── session.py           # Runtime session object with lazy load methods
├── auth.py              # Login, user registration, and hint logic
├── security.py          # Encryption, salt generation, hashing, and key derivation
├── utils.py             # Password suggestion and validation logic
├── vault.py             # Vault load and save logic
├── config.py            # Path configuration
├── test_project.py      # Unit tests for modules
├── data/                # Runtime data (ignored by git)
│   ├── credentials.csv  # App login data
│   ├── app.salt         # App salt for key derivation
│   └── vaults/          # User vaults storage
├── requirements.txt     # Non-built-in Python libraries
└── README.md            # This file
``
