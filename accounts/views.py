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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.hashers import make_password


User = get_user_model()
# Create your views here.
def register_new_user(request):
    """
    Register new user and check for input validation
        - If email exist raise Integrity error
        - Otherwise create new user and login
    """
    form = RegisterForm(request.POST)
    if form.is_valid():
        existing_user = User.objects.filter(email=form.cleaned_data['email'])

        if existing_user.exists():
            return JsonResponse({'exists': existing_user.exists()})
        else:
            newly_created_user = User.objects.create(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                username = form.cleaned_data['email'],
                password = make_password(form.cleaned_data['password']),
                phone_number = form.cleaned_data['phone_number']
            )
            return redirect("login")
    
    return render(request, 'index.html', {"form": form})


def login(request):
    return render(request, 'login.html')