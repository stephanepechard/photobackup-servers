#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# system
import getpass
import hashlib
import re
import uuid


def find_secret_key():
    secret_key = 'None'
    regex = re.compile("^SECRET_KEY = '(.*)'")
    with open('photobackup_server/settings.py', 'r') as settings:
        for line in settings:
            result = regex.search(line)
            if result:
                secret_key = result.group(1)
                break
    return secret_key


def main():
    # ask for the ALLOWED_HOST
    host = input("The host (ex: example.com): ")

    # ask for the upload directory (should be writable by the server)
    media_root = input("The directory where to put the pictures (should be writable by the server): ")

    # ask a password for the server
    password = getpass.getpass(prompt='The server password: ')
    passhash = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # create a distinct string and create a new SECRET_KEY
    unique_id = uuid.uuid4()
    new_secret_key = str(unique_id) + find_secret_key() + str(unique_id)

    filename = 'photobackup_server/photobackup_settings.py'
    with open(filename, 'w') as settings:
        settings.write("# generated settings file for PhotoBackup Django server\n")
        settings.write("ALLOWED_HOSTS = ['{}']\n".format(host))
        settings.write("MEDIA_ROOT = '{}'\n".format(media_root))
        settings.write("SECRET_KEY = '{}'\n".format(new_secret_key))
        settings.write("SERVER_PASSWORD = '{}'\n".format(passhash))

if __name__ == '__main__':
    main()
