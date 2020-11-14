#!/usr/bin/env python3

import argparse
import csv
import hashlib
import logging
import requests
import sys

# Parse command line arguments
parser = argparse.ArgumentParser(description='This description is shown when -h or --help are passed as arguments.')
parser.add_argument('-f', '--file', metavar='FILE', required=True, help='CSV file exported from the password manager')
parser.add_argument('-t', '--type', metavar='TYPE', required=True, help='The password manager used for correct mapping of fields', choices=['bitwarden','keepass','lastpass'])
args = parser.parse_args()

# Configure logging both to file and stdout
logging_format = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(filename="breached-passwords-check.log", filemode='a', format=logging_format, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(logging_format, datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
root.addHandler(handler)

logging.info("Looking up passwords against Have I Been Pwned")

passwords_breached = 0
passwords_checked = 0

with open(args.file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    for row in csv_reader:
        # Read fields according to password manager used
        if "bitwarden" in args.type:
            name = row['name']
            password = row['login_password']

        if "keepass" in args.type:
            name = row['Account']
            password = row['Password']

        if "lastpass" in args.type:
            name = row['name']
            password = row['password']

        # Create SHA1 from password
        sha1password = hashlib.sha1(str(password).encode('utf-8')).hexdigest()

        # Use k-Anonymity model against HIBP to search for partial hashes
        prefix = sha1password[:5]
        suffix = sha1password[5:]

        response = requests.get('https://api.pwnedpasswords.com/range/' + prefix)

        passwords_checked += 1

        if suffix.lower() in response.text.lower():
            passwords_breached += 1
            logging.info("Found breached password " + password + " for entry " + name)

logging.info("Checked " + str(passwords_checked) + " passwords and " + str(passwords_breached) + " of them where breached")
