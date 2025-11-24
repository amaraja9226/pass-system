from django.urls import path
from . import views

urlpatterns = [
     path("form/", views.renew_pass_view, name="renew_form"),  # <-- correct function name
     path('receipt/<str:receipt_id>/', views.renew_receipt_view, name='renew_receipt'),
     path("renew/pay/<int:receipt_id>/", views.pay_and_download_pdf, name="pay_and_download_pdf"),
    
    path('update-payment/<int:receipt_id>/', views.update_payment_status, name="update_payment_status"),
    path('pay/<int:receipt_id>/', views.pay_and_download_pdf, name="pay_and_download_pdf"),
    path('renew/receipt/<int:receipt_id>/', views.renew_receipt_pdf, name='renew_receipt_pdf'),
    path("update-payment/<int:renew_pass_id>/", views.update_payment_status, name="update_payment_status"),







]