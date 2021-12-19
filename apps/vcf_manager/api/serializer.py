from rest_framework import serializers
from apps.vcf_manager.models import UploadedFile, Variants


class UploadSerializer(serializers.ModelSerializer):
   
    class Meta():
        model = UploadedFile
        fields = ('file',)

class VariantsSerializer(serializers.ModelSerializer):
   
    class Meta():
        model = Variants
        fields = '__all__'