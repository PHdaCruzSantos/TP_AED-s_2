import time
from sistema.utils import log_time_sequencial, log_time_binaria

def buscar_sequencial(lista, chave, valor):
    for item in lista:
        if getattr(item, chave) == valor:
            return item
    return None

def buscar_binaria(lista, chave, valor):
    lista.sort(key=lambda x: getattr(x, chave))
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if getattr(lista[meio], chave) == valor:
            return lista[meio]
        elif getattr(lista[meio], chave) < valor:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None
