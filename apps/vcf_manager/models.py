from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(blank=False, null=False)

