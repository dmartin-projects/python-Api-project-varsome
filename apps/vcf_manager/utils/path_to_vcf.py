import os,allel
from django.conf import settings

def get_path():

    file_path=''

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

    return file_path