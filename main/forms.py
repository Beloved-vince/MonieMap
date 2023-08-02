from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    user_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Transaction
        fields = '__all__'
       