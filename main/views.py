from django.shortcuts import render
from .models import Transaction
from .forms  import TransactionForm
# from accounts

def user_dashboard(request):
    return render(request, 'home.html')


def history(request):
    """
    Return transaction history to the view in a tabular form
    name: outgoing or incoming name
    finance: income or expenses
    category: income/expenses category type
    date: date 
    amount: outgoing or incoming amount
    """
    return render(request, 'history.html')


def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            form.save()
        else: 
            print(form.errors)
    else:
        form =TransactionForm()
        
    return render(request, 'transaction.html', {'form': form})