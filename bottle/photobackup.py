#!/usr/bin/env python
# stlib
import getpass
import hashlib
import os
import pwd
import shutil
import sys
# pipped
from bottle import abort, request, route, run
from logbook import debug, notice, warn


def create_settings_file():
    filename = 'photobackup_settings.py'
    
    # Python2 compatibility for input()
    try:
        input = raw_input
    except NameError:
        pass

    # ask for the upload directory (should be writable by the server)
    media_root = input("The directory where to put the pictures" +
                       " (should be writable by the server you use): ")
    if not os.path.isdir(media_root):
        notice("Directory {} does not exist, creating it".format(media_root))
        os.mkdir(media_root)
    server_user = input("Owner of the directory [www-data]: ")
    if not server_user:
        server_user = 'www-data'

    try:
        server_user_uid = pwd.getpwnam(server_user).pw_uid
        if os.stat(media_root).st_uid != server_user_uid:
            notice("Changing owner to: ".format(server_user))
            try:
                shutil.chown(media_root, server_user, server_user)
            except AttributeError:
                os.chown(media_root, server_user, server_user)
    except KeyError:
        warn("User {} not found, please check the directory's rights."
             .format(server_user))

    # ask a password for the server
    text = "The server password that you use in the mobile app: "
    password = getpass.getpass(prompt=text)
    passhash = hashlib.sha512(password.encode('utf-8')).hexdigest()

    with open(filename, 'w') as settings:
        settings.write("# generated settings for PhotoBackup Bottle server\n")
        settings.write("MEDIA_ROOT = '{}'\n".format(media_root))
        settings.write("SERVER_PASSWORD = '{}'\n".format(passhash))

    notice("Settings file is created, please launch me again!")
    return media_root, passhash

# import user-created settings for this specific server
try:
    from photobackup_settings import MEDIA_ROOT, SERVER_PASSWORD
    if os.path.isdir(MEDIA_ROOT) and os.path.exists(MEDIA_ROOT):
        notice("pictures directory is " + MEDIA_ROOT)
    else:
        sys.exit("pictures directory " + MEDIA_ROOT + "does not exist!")
except ImportError:
    warn("Can't find photobackup_settings.py file, creating it")
    MEDIA_ROOT, SERVER_PASSWORD = create_settings_file()


# bottle routes
@route('/', method='POST')
def save_image():
    server_pass = request.forms.get('server_pass')
    if server_pass != SERVER_PASSWORD:
        abort(403, "ERROR: wrong password!")

    upfile = request.files.get('upfile')
    if not upfile:
        abort(401, "ERROR: wrong password!")

    path = os.path.join(MEDIA_ROOT, upfile.raw_filename)
    if not os.path.exists(path):
        debug("upile path: " + path)
        upfile.save(path)
    else:
        warn("file already exists")


@route('/')
def root_route():
    return "Some photobackup documentation"


def main():
    run(host='localhost', reloader=True)


if __name__ == '__main__':
    main()
