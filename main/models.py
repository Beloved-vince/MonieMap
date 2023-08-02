from django.db import models

# Create your models here.

class Transaction(models.Model):
    name = models.CharField(max_length=200)
    transactionType = models.CharField(max_length=10)
    select_type = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now=True)
