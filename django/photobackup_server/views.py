# system
import hashlib
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
# django
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseBadRequest, HttpResponseServerError
# local settings
from photobackup_settings import PASSWORD, MEDIA_ROOT


# Get an instance of a logger
logger = None
try:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    time_format = '%(asctime)s [%(levelname)s] %(message)s'
    formatter = logging.Formatter(time_format)
    logfile = os.path.join(MEDIA_ROOT, 'photobackup-server.log')
    file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except IOError:
    pass


def save_file(upfile):
#    import ipdb;ipdb.set_trace()
    path = os.path.join(MEDIA_ROOT, upfile.name)
    try:
        with open(path, 'wb') as dest:
            if upfile.multiple_chunks:
                for c in upfile.chunks():
                    dest.write(c)
            else:
                dest.write(upfile.read())
            dest.close()
        return True
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return False


def up_view(request):
    if not logger:
        return HttpResponseServerError() # 500

    response = HttpResponseBadRequest() # 400
    if request.method == 'POST':
        if 'password' in request.POST.keys():
            password = request.POST['password']
            response = HttpResponseForbidden() # 403
            if password == PASSWORD:
                if 'upfile' in request.FILES.keys():
                    upfile = request.FILES['upfile']
                    if save_file(upfile):
                        response = HttpResponse() # 200
                        logger.info("successfully saved: {}".format(upfile.name))
                    else:
                        logger.error("error writing file, failing!")
                else:
                    logger.error("no file into FILES dict, failing!")
                    logger.info(request.FILES)
            else:
                logger.error("bad password, failing!")
                logger.info(request.POST)
        else:
            logger.error("no pass into POST dict, failing!")
            logger.info(request.POST)
    else:
        logger.error("not a POST request, failing!")
        logger.info(request)

    return response
