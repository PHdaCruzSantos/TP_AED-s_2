import re
import pickle
class WinnerTree:
    def __init__(self, competidores):
        """
        Inicializa a árvore de vencedores com competidores.
        :param competidores: Lista de competidores (ID da partição, valor).
        """
        self.n = len(competidores)
        self.tree = [None] * (2 * self.n)
        self.competidores = competidores
        self._construir_arvore()

    def extrair_letra_numero(self, s):
        """
        Extrai a primeira letra e o primeiro número de uma string.
        :param s: String de entrada.
        :return: Tupla contendo a letra e o número.
        """
        letra = re.search(r'[A-Za-z]', s)
        numero = re.search(r'\d+', s)
        return (letra.group(0) if letra else None, int(numero.group(0)) if numero else None)

    def _construir_arvore(self):
        """
        Constrói a árvore de vencedores com base nos competidores.
        """
        for i in range(self.n):
            self.tree[self.n + i] = i

        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self._comparar_vencedores(self.tree[2 * i], self.tree[2 * i + 1])

    def _comparar_vencedores(self, competidor1, competidor2):
        """
        Compara dois competidores e retorna o índice do vencedor (menor valor).
        """
        if self.competidores[competidor1][1] <= self.competidores[competidor2][1]:
            return competidor1
        return competidor2

    def obter_vencedor(self):
        """
        Retorna o índice do vencedor atual.
        """
        return self.tree[1]

    def atualizar_vencedor(self, novo_valor):
        """
        Atualiza o valor do vencedor e refaz a competição.
        :param novo_valor: Novo valor do vencedor.
        """
        vencedor_atual = self.obter_vencedor()
        self.competidores[vencedor_atual] = novo_valor
        i = self.n + vencedor_atual
        while i > 1:
            i //= 2
            self.tree[i] = self._comparar_vencedores(self.tree[2 * i], self.tree[2 * i + 1])

    def intercalar_particoes_com_winner_tree(self, particoes, arquivo_saida):
        """
        Intercala as partições ordenadas usando a Árvore de Vencedores.
        :param particoes: Lista de caminhos para as partições ordenadas.
        :param arquivo_saida: Caminho do arquivo de saída ordenado.
        """
        arquivos = [open(particao, 'rb') for particao in particoes]

        competidores = []
        for i, arquivo in enumerate(arquivos):
            try:
                entidade = pickle.load(arquivo)
                competidores.append((i, entidade))
            except EOFError:
                pass

        arvore = WinnerTree(competidores)

        with open(arquivo_saida, 'wb') as saida:
            while True:
                vencedor = arvore.obter_vencedor()
                _, entidade_vencedora = arvore.competidores[vencedor]
                pickle.dump(entidade_vencedora, saida)

                try:
                    nova_entidade = pickle.load(arquivos[vencedor])
                    arvore.atualizar_vencedor((vencedor, nova_entidade))
                except EOFError:
                    arvore.atualizar_vencedor((vencedor, float('inf')))

                if all(competidor[1] == float('inf') for competidor in arvore.competidores):
                    break

        for arquivo in arquivos:
            arquivo.close()