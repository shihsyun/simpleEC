from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from customerauth import views


urlpatterns = [
    path('register/', views.CustomerRegister.as_view(),
         name='customer_register'),
    path('login/', views.CustomerLogin, name='customer_login'),
    path('verify_gencode/', views.CustomerVerifyGencode,
         name='customer_verify_gencode'),
    path('verifycode/', views.CustomerVerifyCode,
         name='customer_verifycode'),
    path('logout/', views.CustomerLogout,
         name='customer_logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
