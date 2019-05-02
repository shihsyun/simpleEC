from django.urls import path, include

urlpatterns = [
    path('', include('ecuserauth.urls')),
    path('', include('ecproduct.urls')),
]
