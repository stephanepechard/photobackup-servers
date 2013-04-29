# system
import hashlib
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
# django
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseBadRequest, HttpResponseServerError
# local settings
from photobackup_settings import SERVER_PASSWORD, MEDIA_ROOT


def create_logger():
    # logger creation
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    time_format = '%(asctime)s [%(levelname)s] %(message)s'
    formatter = logging.Formatter(time_format)
    logfile = os.path.join(MEDIA_ROOT, 'photobackup-server.log')
    file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def save_file(upfile):
    path = os.path.join(MEDIA_ROOT, upfile.name)
    with open(path, 'w') as dest:
        if upfile.multiple_chunks:
            for c in upfile.chunks():
                dest.write(c)
        else:
            dest.write(upfile.read())
        dest.close()


def up_view(request):
    logger = None
    try:
        logger = create_logger()
    except IOError:
        return HttpResponseServerError() # 500

    response = HttpResponseBadRequest() # 400
    logger.info("start main view")
    if request.method == 'POST':
        if 'server_pass' in request.POST.keys():
            server_pass = request.POST['server_pass']
            response = HttpResponseForbidden() # 403
            if server_pass == SERVER_PASSWORD:
                if 'upfile' in request.FILES.keys():
                    upfile = request.FILES['upfile']
                    save_file(upfile)
                    response = HttpResponse() # 200
                    logger.info("saved: ".format(upfile.name))
                    logger.info("upload successful :-)")
                else:
                    logger.error("no file into FILES dict, failing!")
            else:
                logger.error("bad password, failing!")
        else:
            logger.error("no pass into POST dict, failing!")
    else:
        logger.error("not a POST request, failing!")

    return response
