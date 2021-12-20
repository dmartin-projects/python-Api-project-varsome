from django.contrib import admin

from apps.vcf_manager import models


admin.site.register(models.UploadedFile)