from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(blank=False, null=False)

class Variants(models.Model):
    CHROM = models.CharField(max_length=250)
    POS   = models.IntegerField()
    ID    = models.CharField(primary_key=True,max_length=250) 
    REF   = models.CharField(max_length=250)
    ALT_1 = models.CharField(max_length=250, blank=True)
    ALT_2 = models.CharField(max_length=250, blank=True)
    ALT_3 = models.CharField(max_length=250, blank=True)
