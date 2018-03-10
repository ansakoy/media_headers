# -*- coding: utf-8 -*-

import json
import argparse

CUSTOM_DETAILS = 'personal_info.json'

# FIELDS
FROM = u'from'
PASSWORD = u'password'
TO = u'to'
SMTP = u'smtp_server'

parser = argparse.ArgumentParser(description='Configure personal data file')
parser.add_argument('-f', '--from_address',
                    type=str,
                    metavar='',
                    help='FROM address')
parser.add_argument('-p', '--password',
                    type=str,
                    metavar='',
                    help='Password for FROM address')
parser.add_argument('-s', '--server',
                    type=str,
                    metavar='',
                    help='SMTP server of FROM address')
parser.add_argument('-t', '--to_address',
                    type=str,
                    metavar='',
                    help='TO address')


def generate_personal_file(from_address, password, server, to_address):
    # Generate personal data file
    data = {FROM: from_address,
            PASSWORD: password,
            SMTP: server,
            TO: to_address}
    with open(CUSTOM_DETAILS, 'w') as handler:
        json.dump(data, handler)
    print('YOUR DATA SAVED TO FILE:'), CUSTOM_DETAILS


if __name__ == '__main__':
    a = parser.parse_args()
    generate_personal_file(a.from_address, a.password, a.server, a.to_address)

