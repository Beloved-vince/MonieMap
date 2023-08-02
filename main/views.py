from django.shortcuts import render
from .models import Transaction
from .forms  import TransactionForm
from django.http import JsonResponse
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


def get_transactions(request):
    transactions = Transaction.objects.all()
    data = [{'name': t.name, 'transactionType': t.transactionType, 'select_type': t.select_type,
             'amount': t.amount, 'date': t.date.strftime('%Y-%m-%d %H:%M:%S')} for t in transactions]
    return JsonResponse(data, safe=False)