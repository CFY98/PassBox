# EXTERNAL LIBRARIES
import pytest

# PASSBOX MODULES
import app.options


# TEST APP.MAIN
def test_main():
    options = app.options.options_map

    assert "1" in options
    with pytest.raises(KeyError):
        app.options.options_map["one"]
