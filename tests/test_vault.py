# PASSBOX MODULES
import core.vault


# TEST CORE/VAULT
def test_vault():
    # REPLACE PATH WITH JSON FILE CORRESPONDING TO USER ON SETUP
    vault_file = "../data/vaults/8125ec0b20eaf79e.json"
    assert core.vault.vault(vault_file)

    fake_file = "../data/vaults/no_vault.json"
    assert not core.vault.vault(fake_file)

    not_json = "../data/vaults/vault.py"
    assert core.vault.vault(not_json) == {}
