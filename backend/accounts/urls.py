from django.urls import path
from .views import profile, login_view, CreateUserView

urlpatterns = [
    path('profile', profile, name='profile'),
    path('login', login_view, name='login'),
    path('register', CreateUserView.as_view(), name='register')
]