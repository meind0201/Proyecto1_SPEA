'''
Created on 8 mar. 2021

@author: migue
'''

import paho.mqtt.client as mqtt
from AsymCrypto import DH


import cmd
from KMS import KMS_

shared_key = None
pubKeyReceived = 0;

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("DH_AP_ESP")
    print("Connected with result code "+str(rc))



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
   



def main():
    cmdInstancia = CmdESP_Virtual(cmd.Cmd)
    cmdInstancia.cmdloop();


class CmdESP_Virtual(cmd.Cmd):
    intro = ' ______  _____ _______      ___      _               _ \n|  ____|/ ____|  __ \ \    / (_)    | |             | |\n| |__  | (___ | |__) \ \  / / _ _ __| |_ _   _  __ _| |\n|  __|  \___ \|  ___/ \ \/ / | | |__| __| | | |/ _` | |\n| |____ ____) | |      \  /  | | |  | |_| |_| | (_| | |\n|______|_____/|_|       \/   |_|_|   \__|\__,_|\__,_|_|'
    prompt = 'ESP_Virtual>>>'

    def do_start(self, args):
        'Lanzar ESP'
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
        print(pubkey)
       
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
