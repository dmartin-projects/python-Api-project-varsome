from django.urls import path
from apps.vcf_manager.api import views



urlpatterns= [
   
    path('upload_files/', views.UploadFileView.as_view()),
    path('', views.VariantListPaginatedAPIView.as_view()),
    path('<str:id>', views.VariantDetailView.as_view()),
    path('update-variant/<str:id>', views.VariantUpdateAPIView.as_view()),
    path('delete-variant/<str:id>', views.VariantDeleteAPIView.as_view()),
    path('add-new-variant/', views.VariantCreateAPIView.as_view())

]