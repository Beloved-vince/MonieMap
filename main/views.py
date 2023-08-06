from django.shortcuts import render
from .models import Transaction
from .forms  import TransactionForm
from django.db  import  models
import json
from decimal import Decimal
import calendar 
from django.db.models.functions import ExtractMonth
from django.contrib.auth import logout
from django.shortcuts import redirect


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
    formatted_data = Transaction.objects.annotate(month=ExtractMonth('date')).values('month').annotate(
        income=models.Sum('amount', filter=models.Q(transactionType='income')),
        expense=models.Sum('amount', filter=models.Q(transactionType='expense'))
    ).order_by('month')
    
    monthly_transactions = {}

    # Calculate balance for each month
    for entry in formatted_data:
        # entry['balance'] = float(entry['income'] - entry['expense'])
        entry['month'] = calendar.month_name[entry['month']]
        income =round(float( entry['income']) if entry['income'] else 0, 2)
        expense = round(float(entry['expense']) if entry['expense'] else 0, 2)
        
        monthly_transactions[entry['month']] = {
            'income': income,
            'expense': expense
        }
    # Prepare the data for rendering in the template, 
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
    total_income = sum(entry['income'] if entry['income'] is not None else 0 for entry in formatted_data)
    total_expenses = sum(entry['expense'] if entry['expense'] is not None else 0 for entry in formatted_data)
    balance = total_income - total_expenses
    
    print(type(total_expenses))

    data_json = json.dumps(data, cls=DecimalJSONEncoder)
    total_json = json.dumps({
        'total_income': str(total_income),
        'total_expenses': str(total_expenses),
        'balance': str(balance)
    })
    # monthly_transactions_json = json.dumps(list(monthly_transactions), cls=DecimalJSONEncoder)
    
    print(monthly_transactions)

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
    # Get form request
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        
        print(request.user)
        if form.is_valid():
            form.instance.user = request.user
            
            form.save()
        else: 
            print(form.errors)
    else:
        form =TransactionForm()
        
    return render(request, 'transaction.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')