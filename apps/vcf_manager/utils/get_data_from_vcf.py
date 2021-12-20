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
            if len(line)>3: # it avoid empty lines
                result.append(line.split())
            
        result_only_5_fields = [ item[0:5] for item in result ]
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


    file_path=path_to_vcf.get_path()
    result=[]

    if os.path.isfile(file_path):
        
        with open(file_path, 'r') as f:
            data= f.readlines()

        data = [lines.rstrip() for lines in data]

        return data
    else:
        return False
