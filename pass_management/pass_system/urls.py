from django.urls import path
from . import views

urlpatterns = [
    path('validate-receipt/', views.validate_receipt, name='validate_receipt'),

    path('create/', views.create_pass, name='create_pass'),
    path('pass_list/', views.pass_list, name='pass_list'),

    # VIEW RECEIPT BY RECEIPT ID
    path('receipt/<str:receipt_id>/', views.view_receipt, name='view_receipt'),

    # FAKE PAYMENT BUTTON
    path("pay/<str:receipt_id>/", views.fake_payment, name="fake_payment"),

    # PDF DOWNLOAD AFTER PAYMENT
    path("download/<str:receipt_id>/", views.download_receipt_pdf, name="download_receipt_pdf"),
]
