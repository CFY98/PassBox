# PASSBOX MODULES
import core.auth


# TEST CORE.AUTH
def test_auth():
    auth = core.auth.Auth()
    status, session = auth.login("test", "test")
    assert status == "valid"
    assert session is not None

    status, session = auth.login("user", "test")
    assert status == "invalid_user"
    assert session is None

    status, session = auth.login("test", "password")
    assert status == "invalid_password"
    assert session is None

    hint = auth.get_hint("test")
    assert isinstance(hint, str)
    assert auth.get_hint("nouser") is None

    auth.logout()
    assert auth.credentials == {}
