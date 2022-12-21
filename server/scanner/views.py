from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template import loader
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Shopping, Item, Receipt
from .forms import ImageForm
from django.contrib.auth import get_user_model
from .image_processing import scan
import os
import cv2 

def index(request):
    template = loader.get_template('index.html')
    return render(request, 'index.html', {})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def siqn_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data("username")
            password = form.cleaned_data("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index') 

def upload_receipt(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("receipt_image")
            receipt = Receipt(img = img)
            receipt.save()
            
            img_path = receipt.img.path
            context, imgThreshold = scan(img_path)
            if(imgThreshold is not None):
                if os.path.exists(img_path):
                    os.remove(img_path)
                cv2.imwrite(img_path, imgThreshold)

            return render(request, "items_list.html", context)
    else:
        form = ImageForm()
    ctx = {"form": form}
    return render(request, "upload_image.html", ctx)

def view(request):
    shop = Shopping.objects.filter(user_id=request.user.id).values()
    context = { 'shop': shop }
    return render(request, 'view_shopping.html', context)

def purchase(request, id):
    shop = Shopping.objects.filter(user_id=request.user.id).values()
    items = Item.objects.filter(shopping_id=id).values()
    context = { 'shop': shop, 'items': items }
    return render(request, 'purchase.html', context)