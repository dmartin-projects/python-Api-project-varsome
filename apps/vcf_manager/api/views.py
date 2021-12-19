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

import allel
import os

from django.conf import settings


class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

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
        file_path=''

        for filename in os.listdir(settings.MEDIA_ROOT):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            
        
        callset = allel.vcf_to_dataframe( file_path, fields=['CHROM', 'POS','ID','REF','ALT']) 
        queryset = [ vals for vals in callset.to_dict('records')]

        result = list(filter(lambda item: item.get('ID')==id,queryset ))

        if result:
            return HttpResponse(result)
        else:
            raise NotFound(detail="Error 404, page not found", code=404)

class VariantListCreateAPIView(generics.ListCreateAPIView):
    file_path=''

    for filename in os.listdir(settings.MEDIA_ROOT):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
    serializer_class = VariantsSerializer
    callset = allel.vcf_to_dataframe( file_path, fields=['CHROM', 'POS','ID','REF','ALT'])
    queryset = [Variants(**vals) for vals in callset.to_dict('records')]
    pagination_class = SmallSetPagination
    