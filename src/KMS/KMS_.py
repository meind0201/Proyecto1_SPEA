


class KMS_(object):
    masterKey = b'\x16\xd7\x19zl\xc1\xb2(\xce\x0f\x0e\xcb'
    
    newDevices = []
    
    
    def get_masterKey(self): 
        return self.masterKey
    
    def add_device(self, nombre, pubkey):
        nombreDisp = nombre
        clave_pub = pubkey
        obj = {nombreDisp, clave_pub}
        self.newDevices.__add__(obj)
        print(self.newDevices)