# -*- coding: utf-8 -*-

import datetime
import smtplib
from email.mime.text import MIMEText
import schedule
import time
import json
import re

from media_headers import TheEconomist, Bloomberg, WallStreetJournal, Others

PERSONAL_FILE = 'personal_info.json'  # File containing personal mail data. Must be first configured using personal.py


def load_json(json_file):
    # Load JSON file
    with open(json_file, 'r') as data:
        dictionary = json.load(data)
        return dictionary


def dump_json(dictionary, fname):
    # Dump JSON file
    with open(fname, 'w') as handler:
        json.dump(dictionary, handler)

# Load personal data

personal_data = load_json(PERSONAL_FILE)

FROM = personal_data['from']
PASSWORD = personal_data['password']
SMTP_SERVER = personal_data['smtp_server']
TO = personal_data['to']

# CUSTOM GLOBALS

TXT_FILENAME = 'headers.txt'
JSON_FILENAME = 'words_rating.json'
TIME = '19:41'


def extract_data():
    # Scrape headers and write a TXT file
    handler = open(TXT_FILENAME, 'w', encoding='utf-8')
    handler.write(str(datetime.datetime.now()) + '\n\n')
    economist = TheEconomist(handler)
    economist.process_headers()
    bloomberg = Bloomberg(handler)
    bloomberg.process_headers()
    wsj = WallStreetJournal(handler)
    wsj.process_headers()
    others = Others(handler)
    others.walk_through()
    handler.close()


def send_email(filename):
    # Send headers to an email
    handler = open(filename, 'r', encoding="utf8")
    msg = MIMEText(handler.read())
    handler.close()
    msg['Subject'] = 'HEADERS ' + str(datetime.datetime.now())
    msg['From'] = FROM
    msg['To'] = TO
    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASSWORD)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def parse_txt(source):
    # parse TXT file to find most common words excluding those in 'words_to_exclude.json'
    exclude = load_json('words_to_exclude.json')
    handler = open(source, 'r', encoding='utf-8')
    reader = handler.readlines()
    results = dict()
    for line in reader[1:]:
        if not line.startswith('http'):
            lst = re.findall(r"[\w']+", line)
            for word in lst:
                word = word.lower()
                if word not in exclude:
                    if word in results:
                        results[word] += 1
                    else:
                        results[word] = 1
    length = len(results)
    output = dict()
    while length > 0:
        max_val = 2
        max_key = ''
        for entry in results:
            if results[entry] > max_val:
                max_val = results[entry]
                max_key = entry
                output[max_key] = max_val
        try:
            results.pop(max_key)
        except KeyError:
            break
        length -= 1
    handler.close()
    return output


def handle_json(fname, result):
    # Update or create a json file with word ratings
    utc = str(datetime.datetime.utcnow())
    try:
        data = load_json(fname)
        data[utc] = result
        dump_json(data, fname)
    except FileNotFoundError:
        data = {utc: result}
        dump_json(data, fname)


def deliver_headers():
    # scheduled actions
    extract_data()
    send_email(TXT_FILENAME)
    today_summary = parse_txt(TXT_FILENAME)
    handle_json(JSON_FILENAME, today_summary)

if __name__ == '__main__':
    # schedule.every().hour.do(deliver_headers)
    schedule.every().day.at(TIME).do(deliver_headers)
    while True:
        schedule.run_pending()
        time.sleep(1)
