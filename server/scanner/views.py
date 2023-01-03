import os
import cv2 
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from datetime import datetime
from dateutil import parser

from .forms import UserRegistrationForm
from .models import Shopping, Item, Receipt
from .forms import ImageForm
from .image_processing import scan

def index(request):
    return render(request, 'index.html', {})

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect(reverse('index'))
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
    

def upload_receipt(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("receipt_image")
            receipt = Receipt(img = img)
            receipt.save()
            
            img_path = receipt.img.path
            context, imgThreshold = scan(img_path)
            
            if request.user.is_authenticated:
                date = parser.parse(context['date']) if context['date'] else None
                new_shop = Shopping(user=request.user, shop_name=context['company'], date=date, place=context['address'], full_price=context['full_price'])
                new_shop.save()
                if context['items']:
                    for item in context['items']:
                        new_item = Item(shopping=new_shop, item=item['description'], price=item['price'])
                        new_item.save()
            
            if(imgThreshold is not None):
                imgName = os.path.basename(img_path)
                dirName = os.path.dirname(img_path)
                userDirName = os.path.join(dirName, str(request.user))
                if os.path.exists(img_path):
                    os.remove(img_path)
                if not os.path.exists(userDirName):
                    os.mkdir(userDirName)
                newPath = os.path.join(userDirName, imgName)
                cv2.imwrite(newPath, imgThreshold)

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
    shop = Shopping.objects.filter(id=id).values()
    items = Item.objects.filter(shopping_id=id).values()
    context = { 'shop': shop, 'items': items }
    return render(request, 'purchase.html', context)