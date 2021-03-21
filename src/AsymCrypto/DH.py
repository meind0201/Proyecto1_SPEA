'''
Created on 13 mar. 2021

@author: migue
'''

#Diffie-Hellman
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey as rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.dh import DHParameterNumbers



class DHExchange(object):
    parameters = None
    private_key = None
    public_key = None

    def __init__(self, param = None):
       
        if param == None: 
            self.parameters = dh.generate_parameters(generator=2, key_size=512,backend=default_backend())
            self.private_key = self.parameters.generate_private_key(); 
            self.public_key = self.private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        else :
            self.parameters = DHParameterNumbers(param["p"], param["g"]).parameters(backend=default_backend())
            self.private_key = self.parameters.generate_private_key(); 
            self.public_key = self.private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
      
            # self.public_key = self.private_key.public_key()
      
    def get_public_key_and_param(self): 
        return [self.public_key, self.parameters]
    
    def get_shared_key(self, pubKey_ESP):
        shared_key = self.private_key.exchange(serialization.load_pem_public_key(pubKey_ESP))
        return shared_key