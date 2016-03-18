#!/usr/bin/env python
import datetime
import json
import logging
import os
import subprocess
import time



def run_vclient(vclient_command, update=True):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    template = os.path.join(os.path.dirname(__file__), 'vclient_template.tmpl')
    command = 'vclient -h localhost:3002 -t {0} -c {1}'.format(template,
                                                               vclient_command)
    try:
        result = subprocess.check_output([command], shell=True)
    except subprocess.CalledProcessError:
        result = 'err'
    if not update:
        return result
    # result = '22.600000'
    filepath = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(filepath, 'r+') as f:
        data = json.load(f)
        data[vclient_command.rstrip()] = result.rstrip()
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
    return result


if __name__ == '__main__':
    filepath = os.path.join(os.path.dirname(__file__), 'commands')
    with open(filepath) as f:
        commands = f.readlines()
        while True:
            print('Fetching vclient data from {}'.format(datetime.datetime.now()))
            for command in commands:
                run_vclient(command)
                time.sleep(1)
