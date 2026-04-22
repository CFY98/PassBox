# 🔐 PassBox

PassBox is password manager with a hybrid secruity model to explore how secure systems work. It separates data identification (via hashing) from data protection (via encryption) to ensure both usability and security. 

## 🧠 Features

- Deterministic hashing (hashlib) for stable entry IDs for backup, update, and removal

- Encryption (Fernet) to protect sensitive data

- Decryption only at display time

- Fuzzy search on decrypted values for flexible querying

- Cli-based interface

## 💡 Methodology

```
hash_domain(domain) → {
    "domain": encrypted,
    "username": encrypted,
    "password": encrypted
}
```
- Hashes for consistent lookup

- Encryption for data protection

- Decryption only client-facing operations (display and fuzzy search)

## 🛠️ Technologies

- **Python**: Main programming language

- **hashlib (built-in)**: hashing

- **cryptography**: encryption (Fernet)

- **json**: encrypted data storage

- **csv**: authentication storage

## 🚀 Getting Started

📌 Requirements

- Python 3.x installed on your system

##📦 How to Run

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

4. Run the PassBox:

```
python passbox.py
```

🔹 The script will perform its encryption routine with user input as defined in the code.

##  ⚠️ Security Notes

- Encryption keys are stored locally and must be protected

- Hashes are one-way and cannot be reversed

## ⏱️ Future Improvements

- Session locking after repeated failures

- Flask implementation

## 🗂 Project Structure

```
PassBox
├── auth.py             # Login, password, hints, and logout logic
├── main.py             # Menu logic
├── options.py          # Interface options and function map
├── passbox.py          # Login entry point loop
├── requirements.txt    # List of non-built-in libaries
├── security.py         # Encryption, hashing, vault generation
├── README              # This file
└── LICENSE             # MIT License
```

## 📜 License

This project is licensed under the **MIT license**.
