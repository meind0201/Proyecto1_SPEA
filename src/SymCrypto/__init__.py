try:
    from SymCrypto import FernetCustom as Fernet
except Exception:
    from src.SymCrypto import FernetCustom as Fernet

try:
    from SymCrypto import AEAD
except Exception:
    from src.SymCrypto import AEAD
