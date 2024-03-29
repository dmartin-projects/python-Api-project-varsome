from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator

from rest_framework.parsers import JSONParser
from rest_framework_xml.parsers import XMLParser


from apps.vcf_manager.api.serializer import UploadSerializer
from apps.vcf_manager.utils import utils

import os,re

from django.conf import settings


class UploadFileView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        '''
        you cannot upload more than 1 file, if you try it the previous file will be deleted
        '''

        for filename in os.listdir(settings.MEDIA_ROOT):
          file_path = os.path.join(settings.MEDIA_ROOT, filename)
          try:
            os.unlink(file_path)
          except Exception as e:
              print(e)

        file_serializer = UploadSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return JsonResponse(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerVCFiles(APIView):

    parser_classes = (JSONParser,XMLParser)

    def get_list(self,request,format=None):

        page = request.query_params.get('page') or 1


        data = utils.variants_to_list()

        if data: 

            paginator = Paginator(data, 20)
            page = int(page)


            next_page       = page+1 if page+1>=1 and page+1<=paginator.num_pages else None
            previous_page   = page-1 if page-1>=1 and page-1<=paginator.num_pages else None

            next_page_url     = f'http://127.0.0.1:8000/api/?page={next_page}' if next_page else None
            previous_page_url = f'http://127.0.0.1:8000/api/?page={previous_page}' if previous_page else None
            
            
            data_paginated = paginator.page(page).object_list if page>=1 and page<=paginator.num_pages else "no data available"

            
            result={
                "previous page": previous_page_url,
                "next page": next_page_url,
                "total pages":paginator.num_pages,
                "data":data_paginated
            }
            
            return Response(result,status=status.HTTP_200_OK)
            
        else:
            return Response({"error":{
                "code":404,
                "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
            }}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request):
       
        id = request.query_params.get('id')
        flag = False
        result= []
        data2= utils.file_to_list()

        if not id:
            return self.get_list(request)

        if data2:
            pattern = r"\t"+re.escape(id)+r"\t"
            
            for line in data2:
                if re.search(pattern,line):
                    variant_data=line.split() 
                    result.append({ 
                "CHROM": variant_data[0],
                "POS":variant_data[1],
                "ID":variant_data[2],
                "REF":variant_data[3],
                "ALT":variant_data[4],
            })
                    flag=True
                
            if flag:
                return Response(result,status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":{
             "code":404,
             "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
         }}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):

        auth = request.headers.get('Authorization')

        if auth:

            if auth.split()[1]!=utils.get_token():
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            

        file_path= utils.get_path_to_vcf()

        if os.path.isfile(file_path):

            pattern_CHROM = r"^chr[1-9]$|^chr[1]+[0-9]$|^chr[2]+[0-2]$|^chrX{1}$|^chrY{1}$|^chrM{1}$"
            pattern_POS = r"^\d*$"
            pattern_REF = r"^A{1}$|^T{1}$|^G{1}$|^C{1}$|^\.{1}$"
            pattern_ALT = r"^A{1}$|^T{1}$|^G{1}$|^C{1}$|^\.{1}$"
            pattern_ID = r"^rs\d*$"
            

            if not re.search(pattern_CHROM,request.data.get("CHROM")) or not re.search(pattern_POS,str(request.data.get("POS"))) or not re.search(pattern_REF,request.data.get("REF")) or not re.search(pattern_ALT,request.data.get("ALT")) or not re.search(pattern_ID,request.data.get("ID")):    
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                    

                with open(file_path,'a') as f:
                    f.write(f'\n{request.data.get("CHROM")}\t{request.data.get("POS")}\t{request.data.get("ID")}\t{request.data.get("REF")}\t{request.data.get("ALT")}')

                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"error":{
             "code":404,
             "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
         }}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request):

        ''''
        I asume if i must update a variant it must keep same ID so all fields are updated except ID 
        '''

        id = request.query_params.get('id') 
        data = utils.file_to_list()

        if data:

            auth = request.headers.get('Authorization')

            if auth:

                if auth.split()[1]!=utils.get_token():
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

            flag = False
            file_path= utils.get_path_to_vcf()

            if request.data.get("CHROM") =='' or request.data.get("POS") =='' or request.data.get("REF") == '' or request.data.get("ALT")=='':
                
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                pattern = r"\t"+re.escape(id)+r"\t"
                
                with open(file_path, 'w') as f:
                    for line in data:
                        if len(line)>3:
                            if re.search(pattern,line):
                                f.write(f'\n{request.data.get("CHROM")}\t{request.data.get("POS")}\t{id}\t{request.data.get("REF")}\t{request.data.get("ALT")}')
                                flag=True
                            else:
                                f.write(line+'\n')
            
                if flag:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":{
             "code":404,
             "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
         }}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):
        
        auth = request.headers.get('Authorization')

        if auth:

            if auth.split()[1]!=utils.get_token():
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


        flag = False
        data = utils.file_to_list()
        id = request.query_params.get('id')

        if data:

            file_path= utils.get_path_to_vcf()
            
            pattern = r"\t"+re.escape(id)+r"\t"
            
            with open(file_path, 'w') as f:
                for line in data:
                    if len(line)>3:    
                        if re.search(pattern,line)==None:
                            f.write(line+'\n')
                        else:
                            flag=True
            
            if flag:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":{
             "code":404,
             "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
         }}, status=status.HTTP_404_NOT_FOUND)
