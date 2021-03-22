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
pubkey = None
pubkey_ap = None
nombre = "Default"
client = None
already_connected = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("DH_AP_ESP")
    client.subscribe("AP_ESP_MSG")
    client.subscribe("HMAC")
    print("Connected with result code "+str(rc))



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global symmetric_key
    global authenticated_key
    global opcion
    global hmacCalculado
    global masterKey
    global pubkey
    global pubkey_ap
    global already_connected
    
    if msg.topic == "DH_AP_ESP" and already_connected==False:
        pubkey_ap_tree = ET.fromstring((msg.payload.decode('utf-8')))

        pubkey_ap = bytes.fromhex(pubkey_ap_tree[0].text)
        print(str(pubkey_ap_tree[1].text))
        param = {}
        param["p"] = int(pubkey_ap_tree[1].text)
        param["g"] = int(pubkey_ap_tree[2].text)

        diffie = DH.DHExchange(param=param)
        pubkey = diffie.get_public_key_and_param()[0]

        hashMaster = hashes.Hash(hashes.SHA384(), backend=default_backend())
        masterKey = KMS_.KMS_().get_masterKey()
        hashMaster.update(masterKey)
        hashMaster = hashMaster.finalize()

        print("hashMaster: ", hashMaster)

        shared_key = diffie.get_shared_key(pubkey_ap)

        print("shared ", shared_key)
        xml_iot_pubkey = '<?xml version="1.0"?><root><pubk>{pubkey}</pubk></root>'.format(pubkey=pubkey.hex())
        client.publish("DH_ESP_AP", xml_iot_pubkey, 2, False)

        hmacCalculado = hmac.HMAC(hashMaster, hashes.SHA384(), backend=default_backend())
        hmacCalculado.update(shared_key)
        hmacCalculado = hmacCalculado.finalize()
        authenticated_key = hmacCalculado[0:16]
        symmetric_key = hmacCalculado[16:48]


    elif msg.topic == "AP_ESP_MSG" and already_connected==False:

        print("sym", symmetric_key)

        mensajeCifrado = ET.fromstring((msg.payload.decode('utf-8')))
        mensajeCifrado = bytes.fromhex(mensajeCifrado[0].text)
        if opcion == "AEAD":

            f = AEAD(symmetric_key)
            msgCifrado = f.decrypt(mensajeCifrado, b'\x03R\xc0@\x1d\xbf7\x86\xf1\xce\xbd\x85')
            print(msgCifrado)
        elif opcion == "Fernet":
            f = FernetCustom(symmetric_key)
            msgCifrado = f.decrypt(mensajeCifrado)
            print(msgCifrado)
        already_connected = True
        
    else:
        print(msg.topic + " " + str(msg.payload))


def main():
    cmdInstancia = CmdESP_Virtual(cmd.Cmd)
    cmdInstancia.cmdloop();


class CmdESP_Virtual(cmd.Cmd):
    intro = ' ______  _____ _______      ___      _               _ \n|  ____|/ ____|  __ \ \    / (_)    | |             | |\n| |__  | (___ | |__) \ \  / / _ _ __| |_ _   _  __ _| |\n|  __|  \___ \|  ___/ \ \/ / | | |__| __| | | |/ _` | |\n| |____ ____) | |      \  /  | | |  | |_| |_| | (_| | |\n|______|_____/|_|       \/   |_|_|   \__|\__,_|\__,_|_|\nLance el comando start para ejecutar. Agrege el argumento AEAD o Fernet, segun desee.'
    prompt = 'ESP_Virtual>>>'

    def do_start(self, args):
        'Lanzar ESP'
        
        global opcion
        global nombre
        global client
        if len(args) > 0 :
            opcion = args
          
        
        
        # Inicializamos el cliente
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("public", "public")
        client.connect("public.cloud.shiftr.io", 1883, 60)
        client.loop_start()
        

            #DH_ESP_AP
            #/conexion/nueva"
      
        client.publish("/conexion/nueva", "hi", 2, False)
   
   
    def do_send(self,args):
        global nombre
        global pubkey
        global client
        if len(args) > 0 :
            mensaje = args
        else: mensaje ="hola"
        
        
        if opcion == "AEAD":
            f = AEAD(symmetric_key)
            msgCifrado = f.encrypt(mensaje,b'\x03R\xc0@\x1d\xbf7\x86\xf1\xce\xbd\x85')
       
        elif opcion == "Fernet":
            f = FernetCustom(symmetric_key)
            msgCifrado = f.encrypt(mensaje)
           
        xml_msg = '<?xml version="1.0"?><root><nombre>{nombre}</nombre><msg>{mssg}</msg></root>'.format(nombre=pubkey.hex(), mssg = msgCifrado.hex())
        client.publish("/nuevoMensaje", xml_msg, 2, False)
    
        
        
    
    def do_exit(self,args):

        print("Exiting successfully")
        return True


if __name__ == '__main__':
    main()
