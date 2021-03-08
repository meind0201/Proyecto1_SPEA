'''
Created on 8 mar. 2021

@author: migue
'''

import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("public","public")

    client.connect("public.cloud.shiftr.io", 1883, 60)
    client.loop_start()
    while True:
        client.publish("hola", "Hola Mundo", 2, False)
# Inicia una nueva hebra
client.publish("SPEAFM/primerMensaje", "Hola Mundo", 2, False)