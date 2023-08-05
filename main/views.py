from django.shortcuts import render
from .models import Transaction
from .forms  import TransactionForm
from django.db.models.functions import TruncMonth
from django.db  import  models

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
    """
    Return total of income, expenses and balance for each month
    
    Group transactions by month
    """
    monthly_transactions = Transaction.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_income=models.Sum('amount', filter=models.Q(transactionType='income')),
        total_expenses=models.Sum('amount', filter=models.Q(transactionType='expense'))
    ).order_by('month')

    # Calculate balance for each month
    for entry in monthly_transactions:
        entry['balance'] = entry['total_income'] - entry['total_expenses']

    # Prepare the data for rendering in the template
    data = [
        {
            'name': t.name,
            'transactionType': t.transactionType,
            'select_type': t.select_type,
            'amount': str(t.amount),
            'date': t.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for t in Transaction.objects.all()
    ]

    # Calculate total income, total expenses, and balance across all transactions
    total_income = sum(entry['total_income'] for entry in monthly_transactions)
    total_expenses = sum(entry['total_expenses'] for entry in monthly_transactions)
    balance = total_income - total_expenses

    data_json = json.dumps(data, cls=DecimalJSONEncoder)
    total_json = json.dumps({
        'total_income': str(total_income),
        'total_expenses': str(total_expenses),
        'balance': str(balance)
    })
    # monthly_transactions_json = json.dumps(list(monthly_transactions), cls=DecimalJSONEncoder)



    return render(request, 'home.html', context={'total_json': total_json, 'monthly_transactions': monthly_transactions})



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
