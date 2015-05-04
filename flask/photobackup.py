#!/usr/bin/env python
# stlib
import os
# pipped
from flask import abort, Flask, render_template, request
from logbook import debug, warn
# local
from settings import MEDIA_ROOT, PASSWORD


app = Flask(__name__)


@app.route('/', methods=['POST'])
def save_image():
    password = request.form['password']
    if password != PASSWORD:
        abort(403, "ERROR: wrong password!")

    upfile = request.files['upfile']
    if not upfile:
        abort(401, "ERROR: no file in the request!")

    path = os.path.join(MEDIA_ROOT, upfile.raw_filename)
    if not os.path.exists(path):
        debug("upfile path: " + path)
        upfile.save(path)
    else:
        warn("file " + path + " already exists")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    password = request.forms.get('password')
    if password != PASSWORD:
        abort(403, "ERROR: wrong password!")


if __name__ == '__main__':
    app.debug = True
    app.run()
