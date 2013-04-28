# system
import hashlib
import os
# django
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
# local settings
from photobackup_settings import SERVER_PASSWORD, MEDIA_ROOT


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
    response = HttpResponseBadRequest() # 400
    if request.method == 'POST':
        server_pass = request.POST['server_pass']
        response = HttpResponseForbidden() # 403
        if server_pass == SERVER_PASSWORD:
            upfile = request.FILES['upfile']
            save_file(upfile)
            response = HttpResponse() # 200

    return response
