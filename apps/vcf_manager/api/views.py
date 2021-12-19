from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.exceptions import NotFound


from apps.vcf_manager.api.serializer import UploadSerializer,VariantsSerializer
from apps.vcf_manager.models import Variants
from apps.vcf_manager.api.pagination import SmallSetPagination
from apps.vcf_manager.utils import get_data_from_vcf

import os,json, allel, re
import pandas as pd
import vcf

from django.conf import settings


class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        '''
        you cannot upload more than 1 file if you try it the previousgitttt file will be deleted
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

class VariantDetail(APIView):

    def get(self, request,id):
       
        flag = False
        result= []
        file_path=''

        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

        data = ''
        with open(file_path, 'r') as f:
            data= f.readlines()

        data2 = [lines.rstrip() for lines in data]

        pattern = r"\t"+re.escape(id)+r"\t"
        
        with open(file_path, 'r') as f:
             for line in data2:
                if re.search(pattern,line):
                    result.append(line.split())
                    flag=True
        
        if flag:
            return Response(result,status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class VariantListCreateAPIView(generics.ListCreateAPIView):



    serializer_class = VariantsSerializer

    file_path=''

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.isfile(file_path):
        print(file_path)
        callset = allel.vcf_to_dataframe( file_path, fields=['CHROM', 'POS','ID','REF','ALT'])
        queryset = [Variants(**vals) for vals in callset.to_dict('records')]
        pagination_class = SmallSetPagination
        
    else:
        print(file_path)
        queryset = [Variants("0000",0000,"0000","0","0","0","0")]

    '''
    i am aware is an awfull solution to avoid error raised but
    i had not enough time
    SORRY
    '''
    
class VariantCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):

        file_path=''

        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(file_path,'a') as f:
             f.write(f'\n{request.data.get("CHROM")}\t{request.data.get("POS")}\t{request.data.get("ID")}\t{request.data.get("REF")}\t{request.data.get("ALT")}')

        return Response(status=status.HTTP_201_CREATED)

class VariantUpdateAPIView(APIView):

    def put(self, request):

        # print(self.request.query_params.get('id'))
        # print(request.data)

        # callset = get_data_from_vcf.to_dataframe()
        # queryset = [ vals for vals in callset.to_dict('records')]

        # for variant in queryset:
        #     if variant.get('ID')=='rs62635286':
        #         print(variant)

        file_path=''

        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

        data = ''
        with open(file_path, 'r') as f:
            data= f.readlines()

        data2 = [lines.rstrip() for lines in data]   

        #print(data2[141])

        #data2[141] = ''


        patron = '\trs62635284\t'

        #x = re.search(patron,data2[141])

       
        # for line in data2:
        #     if re.search(patron,line):
        #         print(line+'\n')
        
        with open(file_path, 'w') as f:
             for line in data2:
                 if re.search(patron,line)==None:
                     f.write(line+'\n')
                 
            
        
        

       
        # callset = get_data_from_vcf.to_dataframe()
        # queryset = [ vals for vals in callset.to_dict('records')]

        # result = list(filter(lambda item: item.get('ID')==id,queryset ))

        # if result:
        #     return HttpResponse(result)
        # else:
        #     raise NotFound(detail="Error 404, page not found", code=404)
        return Response({"hi":"hi"})

class VariantDeleteAPIView(APIView):

    def delete(self, request,id):

        flag = False
        file_path=''

        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

        data = ''
        with open(file_path, 'r') as f:
            data= f.readlines()

        data2 = [lines.rstrip() for lines in data]

        pattern = r"\t"+re.escape(id)+r"\t"
        
        with open(file_path, 'w') as f:
             for line in data2:
                if re.search(pattern,line)==None:
                    f.write(line+'\n')
                else:
                    flag=True
        
        if flag:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
                
                