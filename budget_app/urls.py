from django.urls import path
from budget_app import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('signup/', views.signup_view, name='signup' ),
    path('login/', views.login_view, name='login' ),
]
