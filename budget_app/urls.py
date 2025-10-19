from django.urls import path
from budget_app import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('signup/', views.signup_view, name='signup' ),
    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),
    path('dashboard/', views.dashboard_view, name='dashboard' ),
    path('create_category/', views.create_category, name='create_category'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
]
