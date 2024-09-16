import heapq
import os
import pickle
import re
from funcionalidades.arvore_de_vencedores import WinnerTree

def extrair_letra_numero(id_str):
    """
    Extrai a parte alfabética e numérica de um identificador.
    :param id_str: String no formato de 'A101'.
    :return: Tupla com a letra e o número como inteiro.
    """
    match = re.match(r"([A-Za-z]+)(\d+)", id_str)
    if match:
        letra = match.group(1)
        numero = int(match.group(2))
        return letra, numero
    raise ValueError(f"Formato de ID inválido: {id_str}")

def converter_binario_para_texto(arquivo_binario, arquivo_texto, entidade_key='id'):
    """
    Converte um arquivo binário em formato pickle para um arquivo de texto com IDs.
    :param arquivo_binario: Caminho do arquivo binário (.db).
    :param arquivo_texto: Caminho para o arquivo de texto temporário.
    :param entidade_key: Chave usada para identificar as entidades.
    """
    with open(arquivo_binario, 'rb') as bin_file:
        entidades = pickle.load(bin_file)

    with open(arquivo_texto, 'w', encoding='utf-8') as txt_file:
        for entidade in entidades:
            txt_file.write(f"{getattr(entidade, entidade_key)}\n")

def converter_binario_para_texto(arquivo_binario, arquivo_temp, entidade_key):
    """
    Converte um arquivo binário para um arquivo de texto temporário.
    
    :param arquivo_binario: Caminho do arquivo binário.
    :param arquivo_temp: Caminho do arquivo de texto temporário.
    :param entidade_key: Chave de identificação das entidades.
    """
    with open(arquivo_binario, 'rb') as bin_file:
        entidades = pickle.load(bin_file)
    
    with open(arquivo_temp, 'w') as txt_file:
        for entidade in entidades:
            txt_file.write(f"{getattr(entidade, entidade_key)}\n")

def gerar_particoes_selecao_por_substituicao_binario(arquivo_entrada, memoria_max):
    """
    Gera partições ordenadas de um arquivo binário de entrada usando seleção por substituição.

    :param arquivo_entrada: Caminho do arquivo binário de entrada desordenado.
    :param memoria_max: Tamanho máximo de elementos a serem carregados na memória.
    :return: Lista de arquivos de partições ordenadas.
    """
    particoes = []
    contador_particoes = 0

    with open(arquivo_entrada, 'rb') as entrada:
        heap = []
        buffer_saida = []
        
        # Ler os primeiros 'memoria_max' elementos e inserir no heap
        for _ in range(memoria_max):
            try:
                entidade = pickle.load(entrada)
                heapq.heappush(heap, entidade)
            except EOFError:
                break

        while heap:
            menor = heapq.heappop(heap)
            buffer_saida.append(menor)
            
            # Ler o próximo elemento
            try:
                proximo = pickle.load(entrada)
                if proximo >= menor:
                    heapq.heappush(heap, proximo)
                else:
                    # Se o próximo elemento é menor, começa a formar uma nova partição
                    heapq.heappush(heap, proximo)
            except EOFError:
                break

            # Quando o buffer atingir o tamanho máximo, criar uma nova partição
            if len(buffer_saida) >= memoria_max:
                contador_particoes += 1
                nome_particao = f"particao_{contador_particoes}.bin"
                particoes.append(nome_particao)
                with open(nome_particao, 'wb') as particao:
                    for item in buffer_saida:
                        pickle.dump(item, particao)
                buffer_saida = []

        # Escrever os elementos restantes
        if buffer_saida:
            contador_particoes += 1
            nome_particao = f"particao_{contador_particoes}.bin"
            particoes.append(nome_particao)
            with open(nome_particao, 'wb') as particao:
                for item in buffer_saida:
                    pickle.dump(item, particao)

    return particoes
# def ordenar_arquivo_binario(arquivo_binario, memoria_max, entidade_key):
#     """
#     Ordena um arquivo binário usando seleção por substituição e intercalando as partições.
    
#     :param arquivo_binario: Caminho do arquivo binário a ser ordenado.
#     :param memoria_max: Tamanho máximo de elementos a serem carregados na memória.
#     :param entidade_key: Chave de identificação das entidades.
#     """
#     arquivo_temp = 'temp_ordenacao.db'
#     arquivo_temp_ordenado = 'temp_ordenacao_ordenada.db'

#     converter_binario_para_texto(arquivo_binario, arquivo_temp, entidade_key)

#     particoes = gerar_particoes_selecao_por_substituicao(arquivo_temp, memoria_max)

#     # Atualizar o vencedor usando a árvore de vencedores
#     arvore = WinnerTree(particoes)
#     arvore.intercalar_particoes_com_winner_tree(particoes, arquivo_temp_ordenado)

#     with open(arquivo_binario, 'rb') as bin_file:
#         entidades_originais = pickle.load(bin_file)

#     converter_texto_para_binario(arquivo_temp_ordenado, arquivo_binario, entidades_originais, entidade_key)

#     # os.remove(arquivo_temp)
#     # os.remove(arquivo_temp_ordenado)
#     # for particao in particoes:
#     #     os.remove(particao)