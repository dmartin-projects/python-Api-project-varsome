import os,allel
from django.conf import settings

def to_dataframe():
    file_path=''

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.isfile(file_path):
        callset = allel.vcf_to_dataframe( file_path, fields=['CHROM', 'POS','ID','REF','ALT'])
        return callset
    else:
        return False
    # if callset:
    #     return callset
    # else:
    #     return -1