# import time
# from sistema.utils import log_time_ordenacao

def merge_sort(lista, chave):
    # start_time = time.time()
    if len(lista) > 1:
        meio = len(lista) // 2
        esquerda = lista[:meio]
        direita = lista[meio:]

        merge_sort(esquerda, chave)
        merge_sort(direita, chave)

        i = j = k = 0

        while i < len(esquerda) and j < len(direita):
            valor_esquerda = getattr(esquerda[i], chave)
            valor_direita = getattr(direita[j], chave)
            if int(valor_esquerda[1:]) < int(valor_direita[1:]):
                lista[k] = esquerda[i]
                i += 1
            else:
                lista[k] = direita[j]
                j += 1
            k += 1

        while i < len(esquerda):
            lista[k] = esquerda[i]
            i += 1
            k += 1

        while j < len(direita):
            lista[k] = direita[j]
            j += 1
            k += 1
    # log_time_ordenacao(time.time() - start_time)
