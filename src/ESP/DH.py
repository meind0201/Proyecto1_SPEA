'''
Created on 13 mar. 2021

@author: migue
'''

#Diffie-Hellman
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric.dh import DHParameterNumbers
from cryptography.hazmat.backends import default_backend


class DHExchange(object):
    parameters = None
    private_key = None
    public_key = None

    def __init__(self, param):
      
        self.parameters = dh.generate_parameters(generator=2, key_size=512,backend=default_backend())
        self.private_key = self.parameters.generate_private_key(); 
        self.public_key = self.private_key.public_key
     
    def get_public_key_and_param(self): 
        return [self.public_key, self.parameters]
    