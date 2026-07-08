# PASSBOX MODULES
import core.auth


# TEST APP.SESSION
def test_session():
    auth = core.auth.Auth()
    _, session = auth.login("test", "test")

    assert session.hmac_key is not None
    assert session.enc_key is not None
    assert isinstance(session.vault_file, str)

    _, session = auth.login("user", "password")
    assert session is None
