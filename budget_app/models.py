from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from datetime import date

# Create your models here.
User = get_user_model()

def current_year():
    return date.today().year

def current_month():
    return date.today().month

class Budget(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        related_name="budgets",
        verbose_name="User",
        on_delete=models.CASCADE
        )
    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    year = models.PositiveIntegerField("Year", default=current_year, editable=False)
    month = models.PositiveIntegerField("Month", default=current_month, editable=False)
    total_limit = models.FloatField("Total Limit", default=0)
    total_spent = models.FloatField("Total Spent", default=0)

    class Meta:
        constraints = [# unique budget per user and month/year
            models.UniqueConstraint(fields=["user", "year", "month"], name="unique_user_budget")
        ]
        ordering = ["-year", "-month"]
    
    def __str__(self):
        return f"{self.user.username} - {self.month:02d}/{self.year}"

class Category(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        related_name="categories",
        verbose_name="User",
        on_delete=models.CASCADE
        )

    budget = models.ForeignKey(
        Budget, 
        related_name="categories",
        verbose_name="Budget",
        on_delete=models.CASCADE
        )

    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    date = models.DateTimeField("Date", auto_now_add=True)
    name = models.CharField("Name", max_length=50)
    limit = models.FloatField("Limit",)
    spent = models.FloatField("Spent", default=0)


    class Meta:
        ordering = ["-date"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}, {self.user.username}"
        

class Transaction(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        related_name="transactions",
        verbose_name="User",
        on_delete=models.CASCADE
        )

    budget = models.ForeignKey(
        Budget, 
        related_name="transactions",
        verbose_name="Budget",
        on_delete=models.CASCADE
        )

    category = models.ForeignKey(
        Category, 
        related_name="transactions",
        verbose_name="Category",
        on_delete=models.CASCADE
        )

    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    date = models.DateTimeField("Date", auto_now_add=True)
    name = models.CharField("Name", max_length=50)
    amount = models.FloatField("Amount")

    class Meta:
        ordering = ["-date"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.name}, {self.amount}, {self.category.name}"
