# PASSBOX MODULES
import core.auth 
from core.security import derive_hmac_key

# USER SESSION
class Session:
    def __init__(self, auth, vault_key, vault_file):
        self.auth = auth
        self.vault_key = vault_key
        self.vault_file =  vault_file
        self._hmac_key = None
    
    @property
    def hmac_key(self):
        if self._hmac_key is None:
            self._hmac_key = derive_hmac_key(self.vault_key)
        return self._hmac_key
