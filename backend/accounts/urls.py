from django.urls import path
from .views import CurrentLoggedInUser, LoginUserView, CreateUserView, refresh_token_view, username_available

urlpatterns = [
    path('profile', CurrentLoggedInUser.as_view(), name='profile'),
    path('login', LoginUserView.as_view(), name='login'),
    path('register', CreateUserView.as_view(), name='register'),
    path('refresh', refresh_token_view, name='refresh'),
    path('validate-username', username_available, name='validate-username')
]