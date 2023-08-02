from django.urls import path
from . import views

urlpatterns = [
    path("current_streak/", views.user_dashboard, name="streak"),
    path('transaction/', views.transaction, name='transaction'),
    path('history/', views.history, name='history'),
    path('add-transaction/', views.transaction, name='add_transaction'),
]