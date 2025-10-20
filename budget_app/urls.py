from django.urls import path
from budget_app import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('signup/', views.signup_view, name='signup' ),
    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),
    path('dashboard/', views.dashboard_view, name='dashboard' ),
    path('search/', views.search_view, name='search' ),
    path('create_category/', views.create_category, name='create_category'),
    path('create_transaction/<uuid:category_id>/', views.create_transaction, name='create_transaction'),
    path('delete_category/<uuid:category_id>/', views.delete_category, name='delete_category'),
    path('delete_transaction/<uuid:transaction_id>/<uuid:category_id>/', views.delete_transaction, name='delete_transaction'),
    path('create_savings_transaction/<uuid:category_id>/', views.create_savings_transaction, name='create_savings_transaction'),
    path('create_savings_goal/<uuid:category_id>/', views.create_savings_goal, name='create_savings_goal'),
    path('create_budget_limit/', views.create_budget_limit, name='create_budget_limit'),
]
