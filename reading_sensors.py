#!/usr/bin/env python
import json
import subprocess


def run_vclient(vclient_command):
    command = 'vclient -h localhost:3002 -t vclient_template.tmpl -c {}'.format(vclient_command)
    try:
        result = subprocess.check_output([command], shell=True)
    except subprocess.CalledProcessError:
        result = 'err'
    # result = '22.600000'
    with open('data.json', 'r+') as f:
        data = json.load(f)
        data[vclient_command] = result.rstrip()
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
    return result


if __name__ == '__main__':
    with open('commands') as f:
        while True:
            for command in f:
                run_vclient(command)
