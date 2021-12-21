import os
from django.conf import settings
import lxml.etree
import lxml.builder 



def get_token():
    token=''
    with open(settings.TOKEN,'r') as f:
        token = f.readline()
    return token.split('=')[1]


def get_path_to_vcf():

    file_path=''

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
   

    return file_path


def variants_to_list():

    file_path=get_path_to_vcf()
    result=[]

    if os.path.isfile(file_path):
        
        with open(file_path, 'r') as f:
            data= f.readlines()

        data_strip = [lines.split('\t') for lines in data if not lines.startswith('#')]
       
        for line in data_strip:
            if len(line)>3: # it avoid empty lines
                result.append(line)
            
        result_only_5_fields = [item[0:5] for item in result ]
        result_only_5_fields_to_json= []

        for variant in result_only_5_fields:
            result_only_5_fields_to_json.append({ 
                "CHROM": variant[0],
                "POS":variant[1],
                "ID":variant[2],
                "REF":variant[3],
                "ALT":variant[4],
            })
        
        return result_only_5_fields_to_json
    else:
        return False

def file_to_list():

    file_path=get_path_to_vcf()
   

    if os.path.isfile(file_path):
        
        with open(file_path, 'r') as f:
            data= f.readlines()

        data = [lines.rstrip() for lines in data]

        return data
    else:
        return False