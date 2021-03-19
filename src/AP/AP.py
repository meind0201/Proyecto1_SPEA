import paho.mqtt.client as mqtt
import cmd
from AsymCrypto import DH
from cryptography.hazmat.primitives import hashes, hmac
import xml.etree.ElementTree as ET
from cryptography.hazmat.backends import default_backend
from KMS import KMS_
shared_key = None
private_key = None

def on_connect(client, userdata, flags, rc):
    client.subscribe("DH_ESP_AP")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('utf-8')))

    msgRecibido = ET.fromstring(str(msg.payload.decode('utf-8')))
    print(msgRecibido[0].text)
  
  
def main():
    cmdInstancia = CmdAP(cmd.Cmd)
    cmdInstancia.cmdloop();
    

class CmdAP(cmd.Cmd):
    intro = '           _____  \n     /\   |  __ \ \n    /  \  | |__) |\n   / /\ \ |  ___/\n  / ____ \| |\n /_/    \_\_|     \n'

    prompt = 'AP>>>'
    
    def do_start(self, args):
        'Lanzar AP'
         #Inicializamos el cliente
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("public","public")
        client.connect("public.cloud.shiftr.io", 1883, 60)
        client.loop_start()
        
        #Recibe parametros de AP y forma su propias claves
        #por hacer
        
        diffie = DH.DHExchange( param = None )
        pubkey = diffie.get_public_key_and_param()[0]
        self.private_key = diffie.get_priv_key()
        #print(pubkey)
       
        #Mandamos a plataforma
       
        xml_public_key = '<?xml version="1.0"?> <root><pubk> {pubkey}</pubk><\root>'.format(pubkey=pubkey)
        client.publish("DH_AP_ESP", xml_public_key, 2, False)
         
        #Genera clave simetrica
         
        hashMaster = hashes.Hash(hashes.SHA384(), backend=default_backend())
        masterKey = KMS_.KMS_().get_masterKey()
        hashMaster.update(masterKey)
        hashMaster= hashMaster.finalize()
        
        self.shared_key = self.private_key.exchange(pubkey)
        hmacCalculado = hmac.HMAC(hashMaster, hashes.SHA384(), backend=default_backend())
        hmacCalculado.update(self.shared_key)
        hmacCalculado = hmacCalculado.finalize()
        authenticated_key = hmacCalculado[0:16] 
        symmetric_key = hmacCalculado[16:48] 
         
        msg = "hola" 
        
      
         
    def do_ejemplo(self, args):
        
        xmle='<root><data>b"-----BEGIN PUBLIC KEY-----\nMIGaMFMGCSqGSIb3DQEDATBGAkEA/RjM6Su358xSzRO2dLIU5qQL2dIhWkWrf98J\nzjhlNFcszuuFRuV6IIDCFIzRiOUCNPP2CNjR4sXJe5tWZvvGEwIBAgNDAAJAHE/b\nSLMoHayEju6gE2pVQrDZJD9zmwEzyg4vuf0F9kTfnpYE+tu57FCzFwDEWlLU4gni\nCszmHsYG+f25YMQASg==\n-----END PUBLIC KEY-----\n"</data></root>'
        ejemplo = ET.fromstring(xmle)
        print(ejemplo[0].text)
    
        kms = KMS_.KMS_()
        print(kms.get_hola())
     
   
    def do_exit(self,args):
        print("Exiting successfully")
        return True


if __name__ == '__main__':
    main()  

