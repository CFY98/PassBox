# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/):

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Fixed` for any bug fixes.
- `Improved` for performance improvements.

## [[v0.1.1] - 2026-07-08 Update](https://github.com/CFY98/PassBox/compare/v0.1.0...v0.1.1)
### Improved
- Better project structure with integration and unit tests in separate directories.

## [[v0.1.0] - Initial Version](https://github.com/CFY98/PassBox/tree/v0.1.0)
### Added
- Hybrid Encryption model to implement strict separation between authentication, session state, and vault access.
- `Argon2id KDF` integration via argon2-cffi for secure master password hashing and key derivation.
- `HMAC-SHA256` Entry IDs for stable, non-descriptive domain lookups.
- Deferred decryption logic to minimise sensitive data footprint in memory.
- Regex-based pattern search for querying vault entries.
- Runtime management of derived cryptographic keys based on session.
- `Cryptography (Fernet)` for symmetric encryption of vault data.
- Storage is isolated into encrypted per-user vaults.
- Split data storage between `credentials.csv` and JSON vault files.
- Unit and integration tests.
