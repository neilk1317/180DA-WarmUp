"""
This file is primarily the same as the one downloaded from Bruinlearn. The modifications made are for the ping-ponging
of messages where the on_message function is modified so that it immedietely sends a response back if it receives a message
from a specific topic and then increments the counter. In the while loop at the bottom an initial message is sent as this 
client is the one that starts the ping-pong. This can be further expanded to accomedate different users/devices by assigning 
them their own personal identifier through the topic string and performing various commands accordingly.
"""


import paho.mqtt.client as mqtt
import numpy as np


# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/naz")


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')


# The default message callback.
# (won't be used if only publishing, but can still exist)
counter = 0
def on_message(client, userdata, message):
  global counter
  print('Received message: "' + str(message.payload) + '" on topic "' +
        message.topic + '" with QoS ' + str(message.qos))
  if(message.topic == "ece180d/naz"):
    print('Incrementing counter to: ' + str(counter+1))
    counter = counter + 1
    print('Sending response...')
    if counter < 10:
      client.publish("ece180d/neil", "Neil sent a message!", qos=1)
    else:
      client.publish("ece180d/neil", "Neil sent the last message!", qos=1)

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# 4. use subscribe() to subscribe to a topic and receive messages.
# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
sent = False
while True:
  if not sent:
    client.publish("ece180d/neil", "Neil sent the first message!", qos=1)
    sent = True
  if counter == 10:
    break
  pass

# 6. use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()