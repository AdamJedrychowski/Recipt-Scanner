from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from dateutil import parser
from .forms import UserRegistrationForm
from .models import Shopping, Item, Receipt
from .forms import ImageForm
from .image_processing import scan

def index(request):
    return render(request, 'index.html', {})

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
            context = scan(img_path)
            
            if request.user.is_authenticated:
                date = parser.parse(context['date']) if context['date'] else None
                new_shop = Shopping(user=request.user, shop_name=context['company'], date=date, place=context['address'], full_price=context['full_price'])
                new_shop.save()
                if context['items']:
                    for item in context['items']:
                        new_item = Item(shopping=new_shop, item=item['description'], price=item['price'])
                        new_item.save()
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