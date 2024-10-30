import os
import uuid

from ELEC9609 import settings
from ELEC9609.API.Modules.Base import *
from ELEC9609.Tools.Logger import TLogger


def func_upload_file(request):
    if not request.method == 'POST':
        return get_result(FALSE, None, f'Invalid request method: {request.method}')
    if not request.FILES:
        return get_result(FALSE, None, f'No file upload')
    if not 'file' in request.FILES:
        return get_result(FALSE, None, f'File need use key 'f'file'f' to upload')
    auth = get_authorisation({'token': request.headers['token']} if 'token' in request.headers else {})
    if auth['error_code'] != SUCCESS:
        return auth
    try:
        file = request.FILES['file']
        file_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'{datetime.timestamp(datetime.now())} {uuid.uuid4()}')
        if file.name and '.' in file.name:
            filename = f'{file_uuid}.{file.name.split('.')[-1]}'
        else:
            filename = f'{file_uuid}'
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return get_result(SUCCESS, {'url': settings.MEDIA_URL + filename}, f'file uploaded: {filename}')
    except Exception as e:
        error_msg = f'upload_file: save file failed: {e}'
        TLogger.terror(error_msg)
        return get_result(FALSE, None, error_msg)
