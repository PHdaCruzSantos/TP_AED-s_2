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

    def atualizar_vencedor(self, indice):
        """
        Atualiza a árvore de vencedores após a remoção do vencedor atual.
        """
        pos = (self.n + indice) // 2
        while pos > 0:
            esquerda = self.tree[2 * pos]
            direita = self.tree[2 * pos + 1]
            self.tree[pos] = self._comparar_vencedores(esquerda, direita)
            pos //= 2

    def intercalar_particoes_com_winner_tree(self, particoes, arquivo_saida):
        """
        Intercala as partições usando a árvore de vencedores e gera um arquivo final ordenado.
        :param particoes: Lista de caminhos das partições.
        :param arquivo_saida: Caminho do arquivo de saída ordenado.
        """
        arquivos = [open(particao, 'rb') for particao in particoes]
        competidores = []

        # Inicializar competidores com o primeiro elemento de cada partição
        for i, arquivo in enumerate(arquivos):
            try:
                entidade = pickle.load(arquivo)
                competidores.append((i, int(entidade.id), entidade))
            except EOFError:
                competidores.append((i, float('inf'), None))

        self.__init__(competidores)

        with open(arquivo_saida, 'wb') as saida:
            while True:
                vencedor_indice = self.obter_vencedor()
                vencedor_particao, _, vencedor_entidade = self.competidores[vencedor_indice]

                if vencedor_entidade is None:
                    break

                pickle.dump(vencedor_entidade, saida)

                try:
                    nova_entidade = pickle.load(arquivos[vencedor_particao])
                    self.competidores[vencedor_indice] = (vencedor_particao, int(nova_entidade.id), nova_entidade)
                except EOFError:
                    self.competidores[vencedor_indice] = (vencedor_particao, float('inf'), None)

                self.atualizar_vencedor(vencedor_indice)

        for arquivo in arquivos:
            arquivo.close()