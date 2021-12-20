from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator


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
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VariantDetailView(APIView):

    def get(self, request,id):
       
        flag = False
        result= []
        data2= utils.file_to_list()

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

        

class VariantListPaginatedAPIView(APIView):


    def get(self,request):

        page = self.request.query_params.get('page') or 1
        data = utils.variant_to_list()

        if data: 

            paginator = Paginator(data, 20)
            page = int(page)


            next_page       = page+1 if page+1>=1 and page+1<=paginator.num_pages else None
            previous_page   = page-1 if page-1>=1 and page<=paginator.num_pages else None

            next_page_url     = f'http://127.0.0.1:8000/api/?page={next_page}' if next_page else None
            previous_page_url = f'http://127.0.0.1:8000/api/?page={previous_page}' if previous_page else None
            
            
            data_paginated = paginator.page(page).object_list if page>=1 and page<=paginator.num_pages else "no data available"

            result={
                "previous page": previous_page_url,
                "next page": next_page_url,
                "total pages":paginator.num_pages,
                "data":data_paginated
            }

            return Response(result,status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":{
             "code":404,
             "message": "VCF file not found, please use http://127.0.0.1:8000/api/upload_files/ end-point to upload your file"
         }}, status=status.HTTP_404_NOT_FOUND)
    
class VariantCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):

        auth = request.META['HTTP_AUTHORIZATION']

        if auth.split()[1]!=utils.get_token().split('=')[1]:
            return Response(status=status.HTTP_403_FORBIDDEN)
            

        file_path=file_path= utils.get_path_to_vcf()

        if os.path.isfile(file_path):

            # pattern_CHROM = r"^chr[1-22]|[X,Y,M]"
            # pattern_POS = r"\t"+re.escape(id)+r"\t"
            # pattern_REF = r"\t"+re.escape(id)+r"\t"
            # pattern_ALT = r"\t"+re.escape(id)+r"\t"
            # pattern_ID = r"\t"+re.escape(id)+r"\t"
            

            if request.data.get("CHROM") =='' or request.data.get("POS")=='' or request.data.get("REF") == '' or request.data.get("ALT")=='':
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


class VariantUpdateAPIView(APIView):

    def put(self, request,id):

        ''''
        I asume if i must update a variant it must keep same ID so all fields are updated except ID 
        '''

        id = id 
        data = utils.file_to_list()

        if data:

            auth = request.META['HTTP_AUTHORIZATION']

            if auth.split()[1]!=utils.get_token().split('=')[1]:
                return Response(status=status.HTTP_403_FORBIDDEN)

            flag = False
            file_path= utils.get_path_to_vcf()

            if request.data.get("CHROM") =='' or request.data.get("POS") =='' or request.data.get("REF") == '' or request.data.get("ALT")=='':
                print('heyyyyyyy!!')
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

       

class VariantDeleteAPIView(APIView):

    def delete(self, request,id):

        auth = request.META['HTTP_AUTHORIZATION']

        if auth.split()[1]!=utils.get_token().split('=')[1]:
            return Response(status=status.HTTP_403_FORBIDDEN)


        flag = False
        data = utils.file_to_list()

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

                
                