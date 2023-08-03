from django.shortcuts import render
from .models import Transaction
from .forms  import TransactionForm
import json
# from accounts

import json
from decimal import Decimal
from django.http import JsonResponse

class DecimalJSONEncoder(json.JSONEncoder):
    """ JSON Encoder """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def user_dashboard(request):

    transactions = Transaction.objects.all()
    data = [
        {
            'name': t.name,
            'transactionType': t.transactionType,
            'select_type': t.select_type,
            'amount': str(t.amount),
            'date': t.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for t in transactions
    ]
 
    #Calculate total income, total expenses, and balanace and return a json object
    total_income = Decimal(0)
    total_expenses = Decimal(0)
    for datum in data:
        if datum['transactionType'] == 'income':
            total_income += Decimal(datum['amount'])
        elif datum['transactionType'] == 'expense':
            total_expenses += Decimal(datum['amount'])
    
    balance = total_income - total_expenses
    
    data_json = json.dumps(data, cls=DecimalJSONEncoder)
    total_json = json.dumps({
        'total_income': str(total_income),
        'total_expenses': str(total_expenses),
        'balance': str(balance)
    })

    return render(request, 'home.html', context={'total_json': total_json})


def history(request):
    """
    Return transaction history to the view in a tabular form
    name: outgoing or incoming name
    transactionType: income or expenses
    select_type: income/expenses category type
    date: date 
    amount: outgoing or incoming amount
    """
    transactions = Transaction.objects.all()
    data = [
        {
            'name': t.name,
            'transactionType': t.transactionType,
            'select_type': t.select_type,
            'amount': str(t.amount),  # Convert Decimal to string
            'date': t.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for t in transactions
    ]

    # Convert the data list to a JSON string using the custom encoder
    data_json = json.dumps(data, cls=DecimalJSONEncoder)
    return render(request, 'history.html', context={'data_json': data_json})


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
