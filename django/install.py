#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# system
import getpass
import grp
import hashlib
import os
import pwd
import re
import stat
import sys
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


def writable_by_user(dirname, username):
    uid = 0
    try:
        uid = pwd.getpwnam(username).pw_uid
    except KeyError:
        print('[ERROR] User {} does not exist!'.format(username))
        return False

    dir_stat = os.stat(dirname)
    if ((dir_stat[stat.ST_UID] == uid) and (dir_stat[stat.ST_MODE] & stat.S_IWUSR)):
        return True

    return False


def writable_by_group(dirname, groupname):
    gid = 0
    try:
        gid = pwd.getpwnam(groupname).pw_gid
    except KeyError:
        print('[ERROR] Group {} does not exist!'.format(groupname))
        return False

    dir_stat = os.stat(dirname)
    if ((dir_stat[stat.ST_GID] == gid) and (dir_stat[stat.ST_MODE] & stat.S_IWGRP)):
        return True

    return False


def main():
    # ask for the ALLOWED_HOST
    host = input("The host (ex: example.com): ")

    # ask for the upload directory (should be writable by the server)
    media_root = input("The directory where to put the pictures (should be writable by the server): ")
    if not os.path.isdir(media_root):
        sys.exit("[ERROR] Directory {} does not exist".format(media_root))

    # test for writability (only for information)
    server_user = 'www-data'
    if not writable_by_user(media_root, server_user) and \
        not writable_by_group(media_root, server_user):
        print('[INFO] Directory {} is not writable by {}, check it!'
                .format(media_root, server_user))

    # ask a password for the server
    password = getpass.getpass(prompt='The server password: ')
    passhash = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # create a distinct string and create a new SECRET_KEY
    unique_id = uuid.uuid4()
    new_secret_key = str(unique_id) + find_secret_key() + str(unique_id)

    filename = 'photobackup_server/photobackup_settings.py'
    with open(filename, 'w') as settings:
        settings.write("# generated settings for PhotoBackup Django server\n")
        settings.write("ALLOWED_HOSTS = ['{}']\n".format(host))
        settings.write("MEDIA_ROOT = '{}'\n".format(media_root))
        settings.write("SECRET_KEY = '{}'\n".format(new_secret_key))
        settings.write("PASSWORD = '{}'\n".format(passhash))

if __name__ == '__main__':
    main()
