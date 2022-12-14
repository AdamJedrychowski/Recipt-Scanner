from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.sign_up, name="signup"),
    path("upload_receipt/", views.upload_receipt, name="upload_receipt"),
    path("view/", views.view, name="view"),
    path("view/<int:id>", views.purchase, name="purchase"),
]