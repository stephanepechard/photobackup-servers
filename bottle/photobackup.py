#!/usr/bin/env python
# stlib
import os
# pipped
from bottle import abort, request, route, run, template
import bottle
from logbook import debug, warn
# local
from settings import MEDIA_ROOT, PASSWORD


app = bottle.default_app()


@route('/', method='POST')
def save_image():
    password = request.forms.get('password')
    if password != PASSWORD:
        abort(403, "ERROR: wrong password!")

    upfile = request.files.get('upfile')
    if not upfile:
        abort(401, "ERROR: no file in the request!")

    path = os.path.join(MEDIA_ROOT, upfile.raw_filename)
    if not os.path.exists(path):
        debug("upfile path: " + path)
        upfile.save(path)
    else:
        warn("file " + path + " already exists")


@route('/')
def index():
    return template('index')


@route('/test')
def test():
    password = request.forms.get('password')
    if password != PASSWORD:
        abort(403, "ERROR: wrong password!")


if __name__ == '__main__':
    run(host='0.0.0.0', reloader=True)
