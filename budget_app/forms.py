from django import forms 
from .models import *

class CreateCategory(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name", "limit"]

class CreateTransaction(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=["name", "amount"]