# PASSBOX MODULES
import app.options
import core.auth
import core.security

# INITIALISE SESSION
auth = core.auth.Auth()
status, session = auth.login("test", "test")


# TEST HELPERS
def _get_deets(session):
    fzf_id = core.security.derive_app_user("test.com", session.hmac_key)
    data = app.options.get_user_vault(session)

    return fzf_id, data


# TEST CORE.OPTIONS
def test_leave(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert app.options.leave()

    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert not app.options.leave()


def test_build_entry():
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    entry = app.options.build_entry("google.com", "user", "pass", key)
    assert "domain" in entry
    assert "username" in entry
    assert "password" in entry


def test_add_entry():
    assert status == "valid"
    fzf_id, data = _get_deets(session)
    entry = app.options.build_entry("google.com", "user", "pass", session.enc_key)
    data.update({fzf_id: entry})
    assert fzf_id in data

    wrong_id = core.security.derive_app_user("gaggle.com", session.enc_key)
    assert wrong_id not in data


def test_view_entries():
    data = app.options.get_user_vault(session)
    assert data is not None
    assert len(data) > 0


def test_delete_entry():
    assert status == "valid"
    fzf_id = core.security.derive_app_user("test.com", session.hmac_key)
    data = app.options.get_user_vault(session)
    data.pop(fzf_id)
    assert fzf_id not in data


def test_update_entry():
    assert status == "valid"
    fzf_id, data = _get_deets(session)
    entry = app.options.build_entry("google.com", "user", "pass", session.enc_key)
    data.pop(fzf_id, None)
    data.update({fzf_id: entry})
    assert fzf_id in data


def test_search_vault():
    import re

    data = app.options.get_user_vault(session)
    seek_entry = "test.com"
    found = False
    for _, creds in data.items():
        domain_key = core.security.decryption(creds["domain"], session.enc_key)
        if re.search(seek_entry, domain_key, re.IGNORECASE):
            found = True
    assert found

    seek_entry = "hello.com"
    found = False
    for _, creds in data.items():
        domain_key = core.security.decryption(creds["domain"], session.enc_key)
        if re.search(seek_entry, domain_key, re.IGNORECASE):
            found = True
    assert not found
