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

def to_list():


    file_path=''
    result=[]

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.isfile(file_path):
        
        with open(file_path, 'r') as f:
            data= f.readlines()

        data_strip = [lines.rstrip() for lines in data if not lines.startswith('#')]
        for line in data_strip:
                result.append(line.split())
            
        result_only_5_fields = [ item[0:5] for item in result ]

        return result_only_5_fields
    else:
        return False
