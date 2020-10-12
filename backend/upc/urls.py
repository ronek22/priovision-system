from django.urls import path
from .views import CreateClientView, get_user_clients_for_current_month, get_user_profit_for_current_month,UpdateClientView

urlpatterns = [
    path('create', CreateClientView.as_view(), name='create_client'),
    path('list', get_user_clients_for_current_month, name='list_clients'),
    path('profit', get_user_profit_for_current_month, name='profit'),
    path('client/<int:pk>/', UpdateClientView.as_view(), name='client_detail_view')
]