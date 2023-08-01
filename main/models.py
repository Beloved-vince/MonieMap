from django.db import models

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )
    name = models.CharField(max_length=200)
    finance = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    select_type = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField(auto_created=True)
    