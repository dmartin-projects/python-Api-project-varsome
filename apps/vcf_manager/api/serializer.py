from rest_framework import serializers
from apps.vcf_manager.models import UploadedFile


class UploadSerializer(serializers.ModelSerializer):
   
    class Meta():
        model = UploadedFile
        fields = ('file',)