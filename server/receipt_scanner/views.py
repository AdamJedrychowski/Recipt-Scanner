from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.views import generic
from django.contrib.auth.forms import UserCreationForm


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def upload_receipt(request):
    template = loader.get_template('upload_image.html')
    return HttpResponse(template.render({}, request))

def view(request):
    pass

def scan(request):
    img = request.POST["image"]
    # machine learning stuff
    return HttpResponseRedirect(reverse('index'))