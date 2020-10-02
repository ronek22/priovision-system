from django.urls import path
from .views import CreateClientView

urlpatterns = [
    path('create', CreateClientView.as_view(), name='create_client')
]