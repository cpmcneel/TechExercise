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

class CreateSavingsTransaction(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=["amount"]
        labels={
            "amount" : ""
        }
class CreateSavingsGoal(forms.ModelForm):
    class Meta:
        model=Category
        fields=["limit"]
        labels={
            "limit" : ""
        }

class CreateBudgetLimit(forms.ModelForm):
    class Meta:
        model=Budget
        fields=["total_limit"]
        labels={
            "total_limit" : ""
        }

class SearchForm(forms.Form):
    month = forms.IntegerField(required=False, label="Month(MM)")
    year = forms.IntegerField(required=False, label="Year(YYYY)")
    term = forms.CharField(required=False, label="Transaction Name") 