from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponse
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

def scan(request):
    pass

def view(request):
    pass