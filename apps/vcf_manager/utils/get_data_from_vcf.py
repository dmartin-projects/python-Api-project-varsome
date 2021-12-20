import os
from apps.vcf_manager.utils  import path_to_vcf

def variant_to_list():


    file_path=path_to_vcf.get_path()
    result=[]

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

def file_to_list():


    file_path=path_to_vcf.get_path()
    result=[]

    if os.path.isfile(file_path):
        
        with open(file_path, 'r') as f:
            data= f.readlines()

        data = [lines.rstrip() for lines in data]

        return data
    else:
        return False
