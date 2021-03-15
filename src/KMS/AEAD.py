from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def cifrar(cadena, key,nonce, AAD):
    #AAD, associated authenticated data, puede ser hmac.
    
    cadena_cifrada =AESGCM.encrypt(nonce.encode(), cadena.encode(), AAD).hex()
    return cadena_cifrada

def descifrar(cadena_cifrada, key, nonce, AAD):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce.encode(), bytes.fromhex(cadena_cifrada) , AAD.encode()).decode()