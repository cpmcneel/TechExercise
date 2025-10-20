from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import *
from .forms import *

# Create your views here.
def ensure_current_budget(user):
    date_today = date.today()
    budget, created = Budget.objects.get_or_create( #check if there is a budget for the current month
                user=user,
                year=date_today.year, 
                month=date_today.month, 
                defaults={"total_limit" : 0}
                )

    if created: #if we needed to create a new budget load previous categories and cost limits to new budget
        Category.objects.create( #create base savings category
            user=user,
            budget=budget,
            name="Savings",
            limit=0
            )   
        last_month = (
            Budget.objects.filter(user=user)
                .exclude(public_id=budget.public_id) 
                .order_by("-year", "-month")
                .first()
            )
        if last_month:
            budget.total_limit=last_month.total_limit
            budget.save()
            for category in last_month.categories.all():
                if category.name != "Savings":
                    Category.objects.create(
                    budget=budget,
                    name=category.name,
                    limit=category.limit
                    )
    else:
        if not Category.objects.filter(budget=budget, name="Savings").exists():
            Category.objects.create(
                user=user,
                budget=budget,
                name="Savings",
                limit=0
            )
    return budget, created


def landing_view(request):
    return render(request, "landing.html")

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ensure_current_budget(user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})  

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("landing")

@login_required(login_url="login")
def dashboard_view(request):#load data and dashboard html
    user = request.user

    date_today = date.today()
    budget, _ = ensure_current_budget(user)
    categories = budget.categories.all()

    category_form = CreateCategory()
    transaction_form = CreateTransaction()
    savings_form = CreateSavingsTransaction()
    savings_goal_form = CreateSavingsGoal()
    budget_limit_form = CreateBudgetLimit()
    savings_category = get_object_or_404(Category, user=request.user, budget=budget, name="Savings")

    row = budget.categories.aggregate(total_limit=Sum("limit"))
    categories_total = row["total_limit"] or 0
    
    context = {
        "user" : user,
        "budget" : budget,
        "categories" : categories,
        "category_form" : category_form,
        "transaction_form" : transaction_form,
        "savings_category" : savings_category,
        "savings_form" : savings_form,
        "savings_goal_form" : savings_goal_form,
        "categories_total" : categories_total,
        "budget_limit_form" : budget_limit_form
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="login")
def create_category(request): #handle category form submition
    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)

            date_today = date.today()
            budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)

            new_category.user = request.user
            new_category.budget = budget
            new_category.save()
    return redirect("dashboard")


@login_required(login_url="login")
def create_transaction(request, category_id): #handle transaction form submition
    if request.method == "POST":
        form = CreateTransaction(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            
            date_today = date.today()
            budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)
            category = get_object_or_404(Category, public_id=category_id, user=request.user)

            new_transaction.user = request.user
            new_transaction.budget = budget
            new_transaction.category = category
            category.spent += new_transaction.amount
            budget.total_spent += new_transaction.amount

            budget.save()
            category.save()
            new_transaction.save()
    return redirect("dashboard")

@login_required(login_url="login")
def delete_category(request, category_id):
    date_today = date.today()
    budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)
    category = get_object_or_404(Category, public_id=category_id, user=request.user)

    budget.total_spent -= category.spent

    budget.save()
    category.delete()
    return redirect("dashboard")
        
@login_required(login_url="login")
def delete_transaction(request, transaction_id, category_id):
    date_today = date.today()
    budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)
    transaction = get_object_or_404(Transaction, public_id=transaction_id, user=request.user)
    category = get_object_or_404(Category, public_id=category_id, user=request.user)

    budget.total_spent -= transaction.amount
    category.spent -= transaction.amount

    budget.save()
    category.save()
    transaction.delete()
    return redirect("dashboard")

@login_required(login_url="login")
def create_savings_transaction(request, category_id): #handle transaction form submition
    if request.method == "POST":
        form = CreateSavingsTransaction(request.POST)
        if form.is_valid():
            new_savings_transaction = form.save(commit=False)
            
            date_today = date.today()
            budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)
            savings_category = get_object_or_404(Category, public_id=category_id, user=request.user)

            budget.total_spent += new_savings_transaction.amount
            new_savings_transaction.user = request.user
            new_savings_transaction.budget = budget
            new_savings_transaction.category = savings_category
            savings_category.spent += new_savings_transaction.amount

            budget.save()
            savings_category.save()
            new_savings_transaction.save()
    return redirect("dashboard")

@login_required(login_url="login")
def create_savings_goal(request, category_id):
    if request.method == "POST":
        savings_category = get_object_or_404(Category, public_id=category_id, user=request.user)
        form = CreateSavingsGoal(request.POST, instance=savings_category)
        if form.is_valid():
            form.save()
        return redirect("dashboard")

@login_required(login_url="login")
def create_budget_limit(request):
    if request.method == "POST":
        date_today = date.today()
        budget = get_object_or_404(Budget, user=request.user, year=date_today.year, month=date_today.month)
        form = CreateBudgetLimit(request.POST, instance=budget)
        if form.is_valid():
            form.save()
        return redirect("dashboard")

@login_required(login_url="login")
def search_view(request):
    
    return render(request, "search.html")