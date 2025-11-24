from django.urls import path
from . import views

urlpatterns = [
     path('', views.auth_view, name='auth_view'),
     path('logout/', views.logout_view, name='logout'),
     path('home/', views.home, name='home'),
     path('check_pass_expiry/', views.check_pass_expiry, name='check_pass_expiry'),
     path('admin/dashboard/login/', views.admin_dashboard_login, name='admin_dashboard_login'),
     path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),


    
    
     

]
