from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import *
from .forms import *

# Create your views here.
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
            date_today = date.today()
            login(request, user)

            budget, created = Budget.objects.get_or_create(
                user=user,
                year=date_today.year, 
                month=date_today.month, 
                defaults={"total_limit" : 0}
                )

            if created:
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
                        Category.objects.create(
                        budget=budget,
                        name=category.name,
                        limit=category.limit
                        )
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})  

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("landing")

@login_required(login_url="login")
def dashboard_view(request):
    user = request.user

    date_today = date.today()
    budget = get_object_or_404(
        Budget,
        user=user,
        year=date_today.year,
        month=date_today.month
        )
    categories = budget.categories.all()
    transactions = budget.transactions.all()

    context = {
        "user" : user,
        "budget" : budget,
        "categories" : categories,
        "transactions" : transactions
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="login")
def create_category(request):
    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)

            date_today = date.today()
            budget = Budget.objects.get(user=request.user, year=date_today.year, month=date_today.month)

            new_category.user = request.user
            new_category.budget = budget
            new_category.save()
    return redirect("dashboard")


@login_required(login_url="login")
def create_transaction(request, category_id):
    if request.method == "POST":
        form = CreateTransaction(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            
            date_today = date.today()
            budget = Budget.objects.get(user=request.user, year=date_today.year, month=date_today.month)
            category = get_object_or_404(Category, public_id=category_id, user=request.user)

            new_transaction.user = request.user
            new_transaction.budget = budget
            new_transaction.category = category
            new_transaction.save()
    return redirect("dashboard")
