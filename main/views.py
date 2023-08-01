from django.shortcuts import render

def user_dashboard(request):
    return render(request, 'home.html')


def history(request):
    return render(request, 'history.html')


def transaction(request):
    return render(request, 'transaction.html')