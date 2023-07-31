from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_new_user, name="register"),
    path('register/login/', views.login, name="login"),
]