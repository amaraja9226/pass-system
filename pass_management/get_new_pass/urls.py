from django.urls import path
from .import views

urlpatterns = [
    # Existing URLs
    path('create/', views.create_application, name='create_application'),
    path('download/<int:app_id>/', views.download_application_pdf, name='download_application_pdf'),

    # New URL for sending to admin
    path('send-to-admin/<int:application_id>/', views.send_to_admin, name='send_to_admin'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.custom_logout, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('reject/<int:app_id>/', views.reject_application, name='reject_application'),
    path('download/<int:app_id>/', views.download_application_pdf, name='download_application_pdf'),
]



   