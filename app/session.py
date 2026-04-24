# PASSBOX MODULES
from core.security import (derive_enc_key, derive_hmac_key)


# USER SESSION
class Session:
    def __init__(self, master_key, vault_file):
        self.master_key = master_key
        self.vault_file = vault_file
        self._hmac_key = None
        self._enc_key = None

    @property
    def hmac_key(self):
        if self._hmac_key is None:
            self._hmac_key = derive_hmac_key(self.master_key)
        return self._hmac_key

    @property
    def enc_key(self):
        if self._enc_key is None:
            self._enc_key = derive_enc_key(self.master_key)
        return self._enc_key
