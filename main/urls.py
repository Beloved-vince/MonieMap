from django.urls import path
from . import views

urlpatterns = [
    path("current_streak/", views.user_dashboard, name="streak"),
]