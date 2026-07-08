# PASSBOX MODULES
import core.auth


# TEST PASSBOX
def test_passbox():
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
