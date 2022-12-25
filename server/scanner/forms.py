from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
 
class ImageForm(forms.Form):
    receipt_image= forms.ImageField()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']
