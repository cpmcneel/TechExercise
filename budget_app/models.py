from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


# Create your models here.
User = get_user_model()

class Budget(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        related_name="budgets",
        verbose_name=_("User"),
        on_delete=models.CASCADE
        )
        
    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    date = models.DateField(_("Date"), auto_now_add=True)
    # Extract year and month from date for search function
    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    total_limit = models.IntegerField(_("Total Limit"))

    class Meta:
        constraints = [# unique budget per user and month/year
            models.UniqueConstraint(fields=["user", "year", "month"], name="unique_user_budget")
        ]
        ordering = ["-year", "-month"]
    
    def __str__(self):
        return f"{self.user.username} - {self.month:02d}/{self.year}"

class Category(models.Model):
    budget = models.ForeignKey(
        Budget, 
        related_name="categories",
        verbose_name=_("Budget"),
        on_delete=models.CASCADE
        )

    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    date = models.DateField(_("Date"), auto_now_add=True)

    # Extract year and month from date for search function
    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    name = models.CharField(_("Name"), max_length=50)
    limit = models.IntegerField(_("Limit"))

    class Meta():
        contraints[ #unique categories in each budget
            models.UniqueConstraint(fields=["budget", "name"], name="unique_user_category"),
        ]
        ordering = ["-date"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f"{self.name}, {self.user.username}"
        

class Transaction(models.Model):
    budget = models.ForeignKey(
        Budget, 
        related_name="categories",
        verbose_name=_("Budget"),
        on_delete=models.CASCADE
        )

    category = models.ForeignKey(
        Category, 
        related_name="transactions",
        verbose_name=_("Category"),
        on_delete=models.CASCADE
        )

    public_id = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    date = models.DateField(_("Date"), auto_now_add=True)
    # Extract year and month from date for search function
    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    name = models.CharField(_("Name"), max_length=50)
    amount = models.IntegerField(_("Amount"))

    class Meta():
        ordering = ["-date"]
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        
    def __str__(self):
        return f"{self.name}, {self.amount}, {self.category.name}"
