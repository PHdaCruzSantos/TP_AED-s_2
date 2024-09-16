import pickle
from funcionalidades.busca import buscar_sequencial
from entidades.imovel import Imovel
from entidades.cliente import Cliente
from entidades.corretor import Corretor
import os
from funcionalidades.selecionar_substituicao import gerar_particoes_selecao_por_substituicao_binario
from funcionalidades.arvore_de_vencedores import WinnerTree

import pickle

class SistemaImobiliaria:
    def __init__(self):
        # Carregar as bases de dados
        self.carregar_dados()

    def carregar_dados(self):
        with open('imoveis.db', 'rb') as f:
            self.imoveis = pickle.load(f)
        with open('clientes.db', 'rb') as f:
            self.clientes = pickle.load(f)
        with open('corretores.db', 'rb') as f:
            self.corretores = pickle.load(f)

    def salvar_dados(self):
        with open('imoveis.db', 'wb') as f:
            pickle.dump(self.imoveis, f)
        with open('clientes.db', 'wb') as f:
            pickle.dump(self.clientes, f)
        with open('corretores.db', 'wb') as f:
            pickle.dump(self.corretores, f)

    def alocar_imovel(self, id_cliente, id_imovel, id_corretor):
        cliente = buscar_sequencial(self.clientes, 'id', id_cliente)
        imovel = buscar_sequencial(self.imoveis, 'id', id_imovel)
        corretor = buscar_sequencial(self.corretores, 'id', id_corretor)
        
        if cliente and imovel and corretor and imovel.status == 'disponível':
            imovel.status = 'alocado'
            corretor.imoveis_gerenciados.append(imovel)
            print(f"Imóvel {imovel.id} alocado ao cliente {cliente.id} pelo corretor {corretor.id}")
        else:
            print("Erro na alocação do imóvel")

    def listar_entidades(self, tipo):
        if tipo == 'imovel':
            for imovel in self.imoveis:
                print(imovel)
        elif tipo == 'cliente':
            for cliente in self.clientes:
                print(cliente)
        elif tipo == 'corretor':
            for corretor in self.corretores:
                print(corretor)
    
    def ordenar_substituicao2(self,arquivo_binario, memoria_max=100, entidade_key='id'):
        """
        Função que faz a ordenação do arquivo binário de dados da imobiliária usando
        seleção por substituição e intercalando com a árvore de vencedores.
        
        :param arquivo_binario: Caminho do arquivo binário a ser ordenado.
        :param memoria_max: Número máximo de entidades que podem ser carregadas na memória.
        :param entidade_key: Chave de identificação das entidades no arquivo binário.
        """
        print("Iniciando ordenação do arquivo binário:")
        particoes = []
        particoes = gerar_particoes_selecao_por_substituicao_binario(arquivo_binario, memoria_max)

        # Atualizar o vencedor usando a árvore de vencedores
        arvore = WinnerTree(particoes)
        arvore.intercalar_particoes_com_winner_tree(particoes, arquivo_binario)

        # for particao in particoes:
        #     os.remove(particao)
        



# class SistemaImobiliaria:
#     def __init__(self):
#         # Inicializar o sistema com carregamento de dados
#         with open('imoveis.db', 'rb') as f:
#             self.imoveis = pickle.load(f)
#         with open('clientes.db', 'rb') as f:
#             self.clientes = pickle.load(f)
#         with open('corretores.db', 'rb') as f:
#             self.corretores = pickle.load(f)
#         # Possivelmente carregar contratos se necessário
#         try:
#             with open('contratos.db', 'rb') as f:
#                 self.contratos = pickle.load(f)
#         except FileNotFoundError:
#             self.contratos = []

    