from django.urls import path
from apps.vcf_manager.api import views



urlpatterns= [
   
    path('upload_files/', views.UploadFileView.as_view()),
    path('', views.VariantListCreateAPIView.as_view()),
    path('<str:id>', views.VariantDetail.as_view())

]