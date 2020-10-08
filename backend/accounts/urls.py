from django.urls import path
from .views import profile, login_view, CreateUserView, refresh_token_view

urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', login_view, name='login'),
    path('register', CreateUserView.as_view(), name='register'),
    path('refresh', refresh_token_view, name='refresh')
]