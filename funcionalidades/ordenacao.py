def merge_sort(lista, chave):
    if len(lista) > 1:
        meio = len(lista) // 2
        esquerda = lista[:meio]
        direita = lista[meio:]

        merge_sort(esquerda, chave)
        merge_sort(direita, chave)

        i = j = k = 0

        while i < len(esquerda) and j < len(direita):
            valor_esquerda = int(getattr(esquerda[i], chave))
            valor_direita = int(getattr(direita[j], chave))
            if valor_esquerda < valor_direita:
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