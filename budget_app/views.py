from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import date

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
            login(request, user)
            todays_date = date.today()

            budget = Budget.objects.filter(
                user=user,
                date__year=todays_date.year,
                date__month=todays_date.month
            )

            if not budget:
                budget = Budget.objects.create(user=user, total_limit=0)

                last_month = (
                    Budget.objects.filter(user=user)
                        .exclude(pk=budget.pk)
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
    context = [
        {"user" : user},
    ]
    return render(request, "dashboard.html", context)