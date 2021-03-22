

class KMS_(object):
    masterKey = b'\x16\xd7\x19zl\xc1\xb2(\xce\x0f\x0e\xcb'
    
    newDevices = {}
    
    
    def get_masterKey(self): 
        return self.masterKey
    
    def add_device(self, pubkeyy = None, sym = None):
        self.newDevices[str(pubkeyy.hex())]={"sym": sym}
        
    def find_sym(self, pubkeyy):
        return self.newDevices[str(pubkeyy.hex())]["sym"]
    
    def list(self):
        print(self.newDevices.keys())
    
    def remove(self):
        cont = 0
        
        apoyo = []
    
        print("Que ESP desea eliminar?\n")
        for key,value in self.newDevices.items():
            cont = cont +1
            apoyo.append(key)
            print(cont, " ", key)
            
        num = input()
        pk = apoyo[int(num)-1]
        del self.newDevices[pk]
        
        