import os

def calcular_numero_particoes(arquivo_entrada, memoria_max):
    """
    Calcula o número de partições que serão geradas com base no tamanho do arquivo e na memória disponível.

    :param arquivo_entrada: Caminho do arquivo de entrada.
    :param memoria_max: Número máximo de elementos que podem ser carregados na memória.
    :return: Número inteiro de partições.
    """
    tamanho_arquivo = os.path.getsize(arquivo_entrada)  # Tamanho em bytes
    tamanho_elemento = 4  # Assumindo que cada elemento seja um número inteiro (4 bytes)
    
    # Estimar o número de elementos no arquivo
    numero_elementos = tamanho_arquivo // tamanho_elemento
    
    # Calcular o número de partições
    numero_particoes = numero_elementos // memoria_max
    
    return max(1, numero_particoes)
