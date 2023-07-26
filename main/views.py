from typing import Any
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import get_template
from engine import settings
from django.db import IntegrityError
from django.contrib.auth import login
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.
def register_new_user(form, request):
    existing_user = User.objects.filter(email=form.cleaned_data['email'])
    
    # Check if email exist before proceeding with the authentication
    if existing_user.exists():
        password_reset_url = request.scheme + '://' + request.get_host() + reverse('password')
        existing_user.first().email_user(
            get_template('emails/already_registered_subject.txt').render(context={'site_name': settings.SITE_NAME}),
            get_template('emails/already_registered.html').render(context={'password_reset_url': password_reset_url})
        )
        raise IntegrityError("Email already exist: %s" % form.cleaned_data['email'])
    else:
        newly_created_user = User.objects.create(
            firstname = form.cleaned_data['firstname'],
            lastname = form.cleaned_data['lastname'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'],
            password_confirm = form.cleaned_data['password_confirm']
        )
    login(request, newly_created_user)
    # return render(request, "index.html")


class RegisterView(FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_url = 'template/home.html'
    
    def get(self, request, *args, **kwargs):
        #Handle GET request
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        
        form = self.form_class(request.POST)
        print("error")
        if form.is_valid():
            try:
                register_new_user(form, request)
                messages.success(request, "Thank you for registering. You will be automatically redirected")
                return HttpResponseRedirect(self.success_url)
            except IntegrityError as e:
                messages.error(request, "An error occurred during registration.")
        else:
            response = requests.get("http://127.0.0.1:8000/register")
            print(form.errors, response.status_code)
        return render(request, self.template_name, {"form": form})