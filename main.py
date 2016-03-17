#!/usr/bin/env python
import json
import os
import subprocess
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


DEBUG = False

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


def read_sensors(device_id):
    command = 'vclient -h localhost:3002 -t ~/thermondo_offsite/vito_temp.tmpl -f ~/thermondo_offsite/command.txt -x ~/thermondo_offsite/vito.sh'
    try:
        results = subprocess.check_output([command], shell=True)
    except subprocess.CalledProcessError:
        results = 'err | err | err | err | err | err |'
    # 23.100000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 3276.699951 |
    result_list = results.split('|')
    result_dict = {
        'temperature': result_list[0],
        'statusStoerung': result_list[1],
        'getError0': result_list[2],
        'getError1': result_list[3],
        'getDevType': result_list[4],
        'getTempKol': result_list[5],
        'getTempWWist': result_list[6],
    }
    return result_dict


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
        device_id = credentials['user']
        sensors_data = read_sensors(device_id)
        # publish temperature data
        message = {
            'meaning': 'Some heating sensors data from our office',
            'value': {
                'temperature': sensors_data['temperature'],
                'status': sensors_data['statusStoerung'],
                'tempKol': sensors_data['getTempKol'],
                'tempWWist': sensors_data['getTempWWist'],
            }
        }
        client.publish(credentials['topic'] + 'data', json.dumps(message))
        time.sleep(publishing_period / 1000.)

if __name__ == '__main__':
    publish_sensor_data(creds, publishing_period)
