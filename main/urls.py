from django.urls import path
from . import views

urlpatterns = [
    path("chart-board", views.user_dashboard, name="chat-board"),
    path('transaction', views.transaction, name='transaction'),
    path('history', views.history, name='history'),
    path('logout', views.logout_view, name='logout'),
    path("", views.user_dashboard, name="home")
    # path('get_transactions/', views.get_transactions, name='get_transactions'),
]