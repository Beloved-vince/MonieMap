from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .forms import RegisterForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login


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

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        try:
            if user is not None:
                print(email, password)
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your homepage URL pattern
            else:
                print('Invalid credentials. Please try again.')
                messages.error(request, 'Invalid credentials. Please try again.')
        except Exception as t:
            return HttpResponse(t)
    return render(request, 'login.html')
