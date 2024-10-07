import heapq
import os
import pickle

def gerar_particoes_selecao_por_substituicao(entidades, memoria_max, tipo_entidade):
    """
    Gera partições ordenadas de uma lista de entidades usando seleção por substituição.

    :param entidades: Lista de entidades desordenadas.
    :param memoria_max: Tamanho máximo de elementos a serem carregados na memória.
    :param tipo_entidade: Tipo da entidade (ex: 'imoveis', 'clientes', 'corretores').
    :return: Lista de arquivos de partições ordenadas.
    """
    particoes = []
    contador_particoes = 0

    # Criar a pasta de partições se não existir
    pasta_particoes = f'particoes/{tipo_entidade}'
    if not os.path.exists(pasta_particoes):
        os.makedirs(pasta_particoes)

    heap = []
    buffer_saida = []
    congelados = []
    
    # Ler os primeiros 'memoria_max' elementos e inserir no heap
    for i in range(min(memoria_max, len(entidades))):
        entidade = entidades[i]
        heapq.heappush(heap, (int(entidade.id), entidade))

    index = memoria_max

    while heap or congelados:
        if heap:
            menor = heapq.heappop(heap)[1]
            buffer_saida.append(menor)
        else:
            menor = None

        # Ler o próximo elemento
        if index < len(entidades):
            proximo = entidades[index]
            index += 1
            if menor is not None and int(proximo.id) >= int(menor.id):
                heapq.heappush(heap, (int(proximo.id), proximo))
            else:
                # Se o próximo elemento é menor, congela o elemento
                congelados.append(proximo)

        # Quando o buffer atingir o tamanho máximo, criar uma nova partição
        if len(buffer_saida) >= memoria_max:
            contador_particoes += 1
            nome_particao = f"{pasta_particoes}/particao_{contador_particoes}.bin"
            particoes.append(nome_particao)
            with open(nome_particao, 'wb') as particao:
                for item in buffer_saida:
                    pickle.dump(item, particao)
            buffer_saida = []

            # Descongelar elementos para a próxima partição
            heap.extend((int(entidade.id), entidade) for entidade in congelados)
            congelados = []
            heapq.heapify(heap)

    # Escrever os elementos restantes
    if buffer_saida:
        contador_particoes += 1
        nome_particao = f"{pasta_particoes}/particao_{contador_particoes}.db"
        particoes.append(nome_particao)
        with open(nome_particao, 'wb') as particao:
            for item in buffer_saida:
                pickle.dump(item, particao)

    return particoes