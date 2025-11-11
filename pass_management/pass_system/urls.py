from django.urls import path
from . import views

urlpatterns = [
    path('validate-receipt/', views.validate_receipt, name='validate_receipt'),
    path('create/', views.create_pass, name='create_pass'),
    path('pass_list/',views.pass_list,name='pass_list')
 
]
