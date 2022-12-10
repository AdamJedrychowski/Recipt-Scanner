from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("upload_receipt/", views.upload_receipt, name="upload_receipt"),
    path("upload_receipt/scan/", views.scan, name="scan"),
    path("view/", views.view, name="view"),
]