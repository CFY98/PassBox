# EXTERNAL LIBRARIES
import pytest

# PASSBOX MODULES
import core.utils


# TEST CORE/UTILS
def test_get_password(monkeypatch):
    monkeypatch.setattr("core.utils.pwinput.pwinput", lambda _: "y")
    password = core.utils.get_password()
    assert isinstance(password, str)


def test_prompt_change(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert core.utils.prompt_pass_change()

    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert not core.utils.prompt_pass_change()


def test_valid_password():
    assert core.utils.valid_password("12ab,.")
    assert not core.utils.valid_password("weak")


def test_strong_password():
    assert core.utils.strong_password(16)

    with pytest.raises(ValueError):
        core.utils.strong_password(4)


def test_confirm_new_pass(monkeypatch):
    monkeypatch.setattr("core.utils.pwinput.pwinput", lambda _: "test")
    assert core.utils.confirm_new_pass("test")

    monkeypatch.setattr("core.utils.pwinput.pwinput", lambda _: "wrong")
    assert not core.utils.confirm_new_pass("test")
