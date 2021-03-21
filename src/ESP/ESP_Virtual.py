'''
Created on 8 mar. 2021

@author: migue
'''

import paho.mqtt.client as mqtt
from AsymCrypto import DH
from cryptography.hazmat.primitives import hashes, hmac
import xml.etree.ElementTree as ET
from cryptography.hazmat.backends import default_backend
import cmd
from KMS import KMS_
from SymCrypto.AEAD import AEAD
from SymCrypto.FernetCustom import FernetCustom
hmacCalculado = None
shared_key = None
pubKeyReceived = 0;
opcion = "Fernet"
symmetric_key = None
authenticated_key = None
masterKey = None
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("DH_AP_ESP")
    client.subscribe("AP_ESP_MSG")
    client.subscribe("HMAC")
    print("Connected with result code "+str(rc))



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    global symmetric_key
    global authenticated_key
    global opcion
    global hmacCalculado
    global masterKey
    if msg.topic == "DH_AP_ESP":
       
        hashMaster = hashes.Hash(hashes.SHA384(), backend=default_backend())
        masterKey = KMS_.KMS_().get_masterKey()
        hashMaster.update(masterKey)
        hashMaster = hashMaster.finalize()
    
        pubkey_ap = ET.fromstring((msg.payload.decode('utf-8')))
        pubkey_ap = bytes.fromhex(pubkey_ap[0].text)
        diffie = DH.DHExchange(param=None)
        shared_key = diffie.get_shared_key(pubkey_ap)
         
           
    elif msg.topic == "HMAC":
        
        hmacCalculado = ET.fromstring((msg.payload.decode('utf-8')))
        hmacCalculado = bytes.fromhex(hmacCalculado[0].text)
           #hmacCalculado = hmac.HMAC(hashMaster, hashes.SHA384(), backend=default_backend())
            #hmacCalculado.update(shared_key)
            #hmacCalculado = hmacCalculado.finalize()
       
        
        print("hmac ", hmacCalculado)
        
    elif msg.topic == "AP_ESP_MSG":
       
        print("sym" ,symmetric_key)
      
        mensajeCifrado = ET.fromstring((msg.payload.decode('utf-8')))
        mensajeCifrado = bytes.fromhex(mensajeCifrado[0].text)
        if opcion == "AEAD":
            
            f = AEAD(symmetric_key)
            msgCifrado = f.decrypt(mensajeCifrado,b'\x03R\xc0@\x1d\xbf7\x86\xf1\xce\xbd\x85')
            print(msgCifrado)
        elif opcion == "Fernet":
            f = FernetCustom(symmetric_key)
            msgCifrado = f.decrypt(mensajeCifrado)
            print(msgCifrado)
       
def main():
    cmdInstancia = CmdESP_Virtual(cmd.Cmd)
    cmdInstancia.cmdloop();


class CmdESP_Virtual(cmd.Cmd):
    intro = ' ______  _____ _______      ___      _               _ \n|  ____|/ ____|  __ \ \    / (_)    | |             | |\n| |__  | (___ | |__) \ \  / / _ _ __| |_ _   _  __ _| |\n|  __|  \___ \|  ___/ \ \/ / | | |__| __| | | |/ _` | |\n| |____ ____) | |      \  /  | | |  | |_| |_| | (_| | |\n|______|_____/|_|       \/   |_|_|   \__|\__,_|\__,_|_|\nLance el comando start para ejecutar. Agrege el argumento AEAD o Fernet, segun desee.'
    prompt = 'ESP_Virtual>>>'

    def do_start(self, args):
        'Lanzar ESP'
        
        global opcion
        if len(args) > 0 :
            opcion = args[0]
        
        
        # Inicializamos el cliente
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("public", "public")
        client.connect("public.cloud.shiftr.io", 1883, 60)
        client.loop_start()
        
        #Recibe parametros de AP y forma su propias claves
        #por hacer
        
        diffie = DH.DHExchange( param = None )
        pubkey = diffie.get_public_key_and_param()[0]
        #print(pubkey)
       
        #Mandamos a plataforma

       #{pubkey}
        xml_public_key = '<?xml version="1.0"?> <root><pubk>{pubkey}</pubk></root>'.format(pubkey=pubkey.hex())
         
            #DH_ESP_AP
            #/conexion/nueva"
        client.publish("/conexion/nueva", xml_public_key, 2, False)
   
   
    def do_ejemplo(self,args):
        kms = KMS_.KMS_()
        print(kms.get_hola())
    
    def do_exit(self,args):

        print("Exiting successfully")
        return True


if __name__ == '__main__':
    main()
