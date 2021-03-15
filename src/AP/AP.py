import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)+",public key: "+str(public_key) )

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("hola")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('utf-8')))

    i=0;
    mensajeRecibido ="";
    payload = str(msg.payload.decode('utf-8'));
    print(payload)
    while payload[i]!='.' and i<len(payload):
        mensajeRecibido = mensajeRecibido + payload[i];
        i+= 1

    mensajeRecibido = int(mensajeRecibido)
    if public_key != mensajeRecibido:  #Recibo la public key del otro nodo
        pubKeyReceived = mensajeRecibido;


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("public","public")

    client.connect("public.cloud.shiftr.io", 1883, 60)
    client.publish("hola",str(public_key)+"/"+"message" , 2, False)
    client.loop_start()
    while True:
        pass
