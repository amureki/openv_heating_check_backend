#!/usr/bin/env python
import json
import os
import time

import paho.mqtt.client as mqtt

creds = {
    'clientId': os.environ.get('RELAYR_CLIENT_ID'),
    'user':     os.environ.get('RELAYR_USER'),
    'password': os.environ.get('RELAYR_PASSWORD'),
    'topic':    os.environ.get('RELAYR_TOPIC'),
    'server':   os.environ.get('RELAYR_SERVER'),
    'port':     os.environ.get('RELAYR_PORT')
}


# ATTENTION !!!
# DO NOT try to set values under 200 ms of the server
# will kick you out
publishing_period = 1000


class MqttDelegate(object):
    "A delegate class providing callbacks for an MQTT client."

    def __init__(self, client, credentials):
        self.client = client
        self.credentials = credentials

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        self.client.subscribe(self.credentials['topic'] + 'cmd')

    def on_publish(self, client, userdata, mid):
        print('Message published.')


def read_sensors_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data


def publish_sensor_data(credentials, publishing_period):
    client = mqtt.Client(client_id=credentials['clientId'])
    delegate = MqttDelegate(client, creds)
    client.on_connect = delegate.on_connect
    client.on_publish = delegate.on_publish
    user, password = credentials['user'], credentials['password']
    client.username_pw_set(user, password)
    try:
        print('Connecting to mqtt server.')
        server, port = credentials['server'], credentials['port']
        client.connect('mqtt.relayr.io', port=1883, keepalive=60)
    except:
        print('Connection failed, check your credentials!')
        return

    # set 200 ms as minimum publishing period
    if publishing_period < 200:
        publishing_period = 200

    while True:
        client.loop()
        # read sensor
        sensors_data = read_sensors_data()
        # publish temperature data
        message = {
            'meaning': 'Some heating data',
            'value': sensors_data
        }
        client.publish(credentials['topic'] + 'data', json.dumps(message))
        time.sleep(publishing_period / 1000.)

if __name__ == '__main__':
    publish_sensor_data(creds, publishing_period)
