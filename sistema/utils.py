import random
import string
import pickle
import os
import time
from entidades.imovel import Imovel
from entidades.cliente import Cliente
from entidades.corretor import Corretor

def gerar_imoveis(quantidade):
    imoveis = [Imovel(str(i), ''.join(random.choices(string.ascii_uppercase, k=10)), random.randint(100000, 1000000), random.choice(['casa', 'apartamento']), 'disponível') for i in range(1, quantidade + 1)]
    random.shuffle(imoveis)  # Desordenar a lista
    return imoveis

def gerar_clientes(quantidade):
    clientes = [Cliente(str(i), ''.join(random.choices(string.ascii_uppercase, k=5)), '123456789', 'email@example.com', {'tipo': 'casa', 'preco_max': 500000}) for i in range(1, quantidade + 1)]
    random.shuffle(clientes)  # Desordenar a lista
    return clientes

def gerar_corretores(quantidade):
    corretores = [Corretor(str(i), ''.join(random.choices(string.ascii_uppercase, k=5)), '123456789', 'email@example.com') for i in range(1, quantidade + 1)]
    random.shuffle(corretores)  # Desordenar a lista
    return corretores

def salvar_dados(imoveis, clientes, corretores):
    if not os.path.exists('db'):
        os.makedirs('db')

    with open('db/imoveis.db', 'wb') as f:
        pickle.dump(imoveis, f)
    with open('db/clientes.db', 'wb') as f:
        pickle.dump(clientes, f)
    with open('db/corretores.db', 'wb') as f:
        pickle.dump(corretores, f)

    
# Funções de log
def log_time_sequencial(exec_time):
    with open('logs/busca_sequencial_log.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Busca Sequencial - Tempo de Execução: {exec_time:.6f} segundos\n")

def log_time_binaria(exec_time):
    with open('logs/busca_binaria_log.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Busca Binária - Tempo de Execução: {exec_time:.6f} segundos\n")

def log_time_ordenacao(exec_time):
    with open('logs/ordenacao_log.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Ordenação - Tempo de Execução: {exec_time:.6f} segundos\n")
