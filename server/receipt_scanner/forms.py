from django import forms
 
class ImageForm(forms.Form):
    receipt_image= forms.ImageField()