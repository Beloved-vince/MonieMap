from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
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
from django.contrib.auth.hashers import make_password


User = get_user_model()
# Create your views here.
def register_new_user(form, request):
    """
    Register new user and check for input validation
        - If email exist raise Integrity error
        - Otherwise create new user and login
    """
    existing_user = User.objects.filter(email=form.cleaned_data['email'])

    if existing_user.exists():
        password_reset_url = request.scheme + '://' + request.get_host() + reverse('password')
        existing_user.first().email_user(
            get_template('emails/already_registered_subject.txt').render(context={'site_name': settings.SITE_NAME}),
            get_template('emails/already_registered.html').render(context={'password_reset_url': password_reset_url})
        )
        raise IntegrityError("Email already exist: %s" % form.cleaned_data['email'])
    else:
        newly_created_user = User.objects.create(
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            password = make_password(form.cleaned_data['password']),
            phone_number = form.cleaned_data['phone_number']
        )
    # login(request, newly_created_user)
    # return render(request, "index.html")


class RegisterView(FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_url = 'login'
    
    def get(self, request, *args, **kwargs):
        #Handle GET request
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs):
        # Handle POST request
        
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                register_new_user(form, request)
                print("success")
                messages.success(request, "Thank you for registering. You will be automatically redirected")
                return redirect('login')
            except IntegrityError as e:
                messages.error(request, "An error occurred during registration.")
        else:
            response = requests.get("http://127.0.0.1:8000/register")
            print(form.errors, response.status_code)
        return render(request, self.template_name, {"form": form})
    

def login(request):
    return render(request, 'login.html')