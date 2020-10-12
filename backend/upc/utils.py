from .models import Client, TypeOfClient
import numpy as np
import decimal

# matrix.item((row, column))
# row: cash, column: counts 
matrix1 = np.mat('0.5 0.8 1 1.2; 0.8 1 1.2 1.4; 1.2 1.2 1.4 1.5')
matrix2 = np.mat('1.5 1.7; 1.7 1.8; 1.8 2.0')

#region New Clients
def calculate_new_clients(clients):
    '''
    New Clients only total
    Profit depends on total_price and ammount of clients 
    '''
    profit = 0.0
    count_threshold = new_client_count_threshold(clients.count())
    for client in clients.all():
        total_threshold = new_client_price_threshold(client.total)
        multiply = matrix1.item((total_threshold,count_threshold)) 
        client_profit = float(client.total)*multiply
        profit += client_profit

    return profit

def new_client_price_threshold(total):
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

#endregion 

#region Old Clients
def calculate_old_clients(clients: Client):
    profit = 0

    for client in clients.all():
        total_thresh = old_total_threshold(client.total)
        core_thresh = old_core_threshold(client.core)
        multiply = matrix2.item((core_thresh, total_thresh))
        client_profit = float(client.total)*multiply
        if core_thresh == 0: client_profit += 3.0
        profit += client_profit
        
    return profit


def old_total_threshold(total):
    if 0.01 <= total <= 25.00:
        return 0
    if total >= 25.01:
        return 1
    return -1  

def old_core_threshold(core):
    if 0.01 <= core <= 9.99:
        return 0
    if 10.00 <= core <= 20.00:
        return 1
    if 20.01 <= core:
        return 2
    return -1

#endregion

def calculate_profit_from_clients(clients: Client):
    # grupuj po typie klienta
    new_clients = Client.objects.filter(type=TypeOfClient.NEW)
    old_clients = Client.objects.filter(type=TypeOfClient.PRESENT)
    
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