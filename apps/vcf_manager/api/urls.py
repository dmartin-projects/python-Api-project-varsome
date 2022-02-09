from django.urls import path
from apps.vcf_manager.api import views

from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns= [
   
    path('upload_files/', views.UploadFileView.as_view()),
    path('', views.ManagerVCFiles.as_view()),

]

#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'xml'])