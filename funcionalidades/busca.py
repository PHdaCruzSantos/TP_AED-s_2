import time
from sistema.utils import log_time_sequencial, log_time_binaria

def buscar_sequencial(lista, chave, valor):
    start_time = time.time()
    for item in lista:
        if getattr(item, chave) == valor:
            log_time_sequencial(time.time() - start_time)
            return item
    log_time_sequencial(time.time() - start_time)
    return None

def buscar_binaria(lista, chave, valor):
    start_time = time.time()
    lista.sort(key=lambda x: getattr(x, chave))
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if getattr(lista[meio], chave) == valor:
            log_time_binaria(time.time() - start_time)
            return lista[meio]
        elif getattr(lista[meio], chave) < valor:
            inicio = meio + 1
        else:
            fim = meio - 1
    log_time_binaria(time.time() - start_time)
    return None
