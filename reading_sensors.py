#!/usr/bin/env python
import json
import subprocess
import os

import time


def run_vclient(vclient_command, update=True):
    command = 'vclient -h localhost:3002 -t vclient_template.tmpl -c {}'.format(vclient_command)
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
        data[vclient_command] = result.rstrip()
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
    return result


if __name__ == '__main__':
    filepath = os.path.join(os.path.dirname(__file__), 'commands')
    with open(filepath) as f:
        commands = f.read()
        while True:
            for command in commands:
                run_vclient(command)
                time.sleep(1)
