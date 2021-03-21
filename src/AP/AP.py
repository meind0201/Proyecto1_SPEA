import paho.mqtt.client as mqtt
import cmd
from AsymCrypto import DH
from cryptography.hazmat.primitives import hashes, hmac
import xml.etree.ElementTree as ET
from cryptography.hazmat.backends import default_backend
from KMS import KMS_
from SymCrypto.AEAD import AEAD
from time import sleep
from SymCrypto.FernetCustom import FernetCustom

shared_key = None
private_key = None
pubkey = None
symmetric_key = None
authenticated_key = None
opcion = "Fernet"
kms = None
param = None
def on_connect(client, userdata, flags, rc):
    client.subscribe("DH_ESP_AP")
    client.subscribe("/conexion/nueva")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global opcion
    global kms
    global param
    if msg.topic == "/conexion/nueva":
        #Mandamos a plataforma
        #print(pubkey)
        xml_public_key = '<?xml version="1.0"?><root><pubk>{pubkey}</pubk><p>{p}</p><g>{g}</g></root>'.format(pubkey=pubkey.hex(), p = param.parameter_numbers().p, g = param.parameter_numbers().g)

        # Conexion con dispositivo IOT
        
        client.publish("DH_AP_ESP", xml_public_key, 2, False)

    elif msg.topic == "/DH_ESP_AP":
        # Genera clave simetrica
      
        hashMaster = hashes.Hash(hashes.SHA384(), backend=default_backend())
        masterKey = kms.get_masterKey()
        hashMaster.update(masterKey)
        hashMaster = hashMaster.finalize()

        # formato==> xmle='<root><data>b"-----BEGIN PUBLIC KEY-----\nMIGaMFMGCSqGSIb3DQEDATBGAkEA/RjM6Su358xSzRO2dLIU5qQL2dIhWkWrf98J\nzjhlNFcszuuFRuV6IIDCFIzRiOUCNPP2CNjR4sXJe5tWZvvGEwIBAgNDAAJAHE/b\nSLMoHayEju6gE2pVQrDZJD9zmwEzyg4vuf0F9kTfnpYE+tu57FCzFwDEWlLU4gni\nCszmHsYG+f25YMQASg==\n-----END PUBLIC KEY-----\n"</data></root>'

        pubkey_iot = ET.fromstring((msg.payload.decode('utf-8')))
        pubkey_iot = bytes.fromhex(pubkey_iot[0].text)
        diffie = DH.DHExchange(param=None)
        shared_key = diffie.get_shared_key(pubkey_iot)
        hmacCalculado = hmac.HMAC(hashMaster, hashes.SHA384(), backend=default_backend())
        hmacCalculado.update(shared_key)
        hmacCalculado = hmacCalculado.finalize()
        authenticated_key = hmacCalculado[0:16]
        symmetric_key = hmacCalculado[16:48]
        print("shared", shared_key)
        
        xml_hmac = '<?xml version="1.0"?><root><pubk>{pubkey}</pubk></root>'.format(pubkey=hmacCalculado.hex())

        client.publish("HMAC", xml_hmac, 2, False)
        sleep(2)
        if opcion == "AEAD":
            f = AEAD(symmetric_key)
            msgCifrado = f.encrypt("Connected",b'\x03R\xc0@\x1d\xbf7\x86\xf1\xce\xbd\x85')
            xml_msgCifrado = '<?xml version="1.0"?> <root><cif>{msgCifrado}</cif></root>'.format(msgCifrado=msgCifrado.hex())
            client.publish("AP_ESP_MSG", xml_msgCifrado, 2, False)
        elif opcion == "Fernet":
            f = FernetCustom(symmetric_key)
            msgCifrado = f.encrypt("Connected")
            xml_msgCifrado = '<?xml version="1.0"?> <root><cif>{msgCifrado}</cif></root>'.format(msgCifrado=msgCifrado.hex())
            client.publish("AP_ESP_MSG", xml_msgCifrado, 2, False)
    else :
        print(msg.topic+" "+str(msg.payload.decode('utf-8')))
      
    
  
def main():
    global kms
    kms = KMS_.KMS_()
    cmdInstancia = CmdAP(cmd.Cmd)
    cmdInstancia.cmdloop();
   
    

class CmdAP(cmd.Cmd):
    intro = '           _____  \n     /\   |  __ \ \n    /  \  | |__) |\n   / /\ \ |  ___/\n  / ____ \| |\n /_/    \_\_|     \n\nLance el comando start para ejecutar. Agrege el argumento AEAD o Fernet, segun desee.'

    prompt = 'AP>>>'
    
    def do_start(self, args):
        'Lanzar AP'
        
        global opcion
        global pubkey
        global param
        
        if len(args) > 0 :
            opcion = args[0]
        

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
       
        pubkey, param = diffie.get_public_key_and_param()
        

      
         
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

