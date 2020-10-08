from .models import Client, TypeOfClient
import numpy as np

# matrix.item((row, column))
# row: cash, column: counts 
matrix = np.mat('0.5 0.8 1 1.2; 0.8 1 1.2 1.4; 1.2 1.2 1.4 1.5')

def calculate_new_clients(clients):
    '''
    New Clients only total
    Profit depends on total_price and ammount of clients 
    '''
    profit = 0
    count_threshold = new_client_count_threshold(clients.count())
    for client in clients:
        total_threshold = new_client_count_threshold(client.total)
        multiply = matrix.item((total_threshold,count_threshold))        
        profit += client.total*multiply

    return profit

    

def calculate_old_clients(clients):
    # matryca 2 na dole total, z lewej core
    # prowizja z core, jak mniejsza od 10 dolicz 3zl
    # matryca 4 premium
    # cala prowizja core + premium
    profit = 0

    pass

def new_client_price_threshold(client):
    total = client.total
    if total < 79.99:
        return 0
    if total < 90.00:
        return 1
    return 2

def new_client_count_threshold(counted):
    if counted < 10:
        return 0
    if counted < 16:
        return 1
    if counted < 21:
        return 2
    return 3 

def calculate_profit_from_clients(clients):
    # grupuj po typie klienta
    new_clients = Clients.objects.filter(type=TypeOfClient.NEW)
    old_clients = Clients.objects.filter(type=TypeOfClient.PRESENT)
    
    # nowy klient tylko total
    # tylko total i to jest cala prowizja
    # wysokosc prowizji zalezna od kwoty i ilosci nowych klientow
    profit_from_new = calculate_new_clients(new_clients)
    # stary klient
    # matryca 2 na dole total, z lewej core
    # prowizja z core, jak mniejsza od 10 dolicz 3zl
    # matryca 4 premium
    # cala prowizja core + premium
    profit_from_old = calculate_old_clients(old_clients)

    pass