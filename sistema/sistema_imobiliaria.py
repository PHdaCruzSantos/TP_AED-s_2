import pickle
from funcionalidades.busca import buscar_sequencial
from entidades.imovel import Imovel
from entidades.cliente import Cliente
from entidades.corretor import Corretor
import os
from funcionalidades.selecionar_substituicao import gerar_particoes_selecao_por_substituicao
from funcionalidades.arvore_de_vencedores import WinnerTree
from funcionalidades.tabela_hash import HashTable

import pickle

class SistemaImobiliaria:
    def __init__(self):
        # Carregar as bases de dados
        self.carregar_dados('imoveis')
        self.carregar_dados('clientes')
        self.carregar_dados('corretores')
        self.hash_table = HashTable("db/clientes.db")

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

    def carregar_dados(self, arq):
        if arq == 'imoveis':
            with open(f'db/{arq}.db', 'rb') as f:
                self.imoveis = pickle.load(f)
        elif arq == 'clientes':
            with open(f'db/{arq}.db', 'rb') as f:
                self.clientes = pickle.load(f)
        elif arq == 'corretores':
            with open(f'db/{arq}.db', 'rb') as f:
                self.corretores = pickle.load(f)

    def salvar_dados(self, arq):
        if arq == 'imoveis':
            with open(f'db/{arq}.db', 'wb') as f:
                pickle.dump(self.imoveis, f)
        elif arq == 'clientes':
            with open(f'db/{arq}.db', 'wb') as f:
                pickle.dump(self.clientes, f)
        elif arq == 'corretores':
            with open(f'db/{arq}.db', 'wb') as f:
                pickle.dump(self.corretores, f)

    

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
    

    def ordenar_arquivo_binario(self, entidades, memoria_max, tipo_entidade):
        """
        Ordena uma lista de entidades usando seleção por substituição e intercalando as partições.
        
        :param entidades: Lista de entidades a serem ordenadas.
        :param memoria_max: Tamanho máximo de elementos a serem carregados na memória.
        :param tipo_entidade: Tipo da entidade (ex: 'imoveis', 'clientes', 'corretores').
        """
        particoes = gerar_particoes_selecao_por_substituicao(entidades, memoria_max, tipo_entidade)

        # Atualizar o vencedor usando a árvore de vencedores
        arvore = WinnerTree(particoes)
        arquivo_saida = f'db/{tipo_entidade}_ordenado.bin'
        arvore.intercalar_particoes_com_winner_tree(particoes, arquivo_saida)

        # for particao in particoes:
        #     os.remove(particao)

        # Copiar a base ordenada em arquivos de texto para conferência
        with open(arquivo_saida, 'rb') as bin_file, open(f"{arquivo_saida}.txt", 'w') as txt_file:
            try:
                while True:
                    entidade = pickle.load(bin_file)
                    txt_file.write(f"{entidade}\n")
            except EOFError:
                pass

    def carregar_clientes_para_hash(self):
        """
        Carrega os clientes existentes na tabela hash.
        """
        for cliente in self.clientes:
            self.hash_table.inserir(cliente.id, cliente)
    
    def inserir_cliente(self, id_cliente, nome, telefone, email, interesse):
        cliente = Cliente(id_cliente, nome, telefone, email, interesse)
        self.hash_table.inserir(cliente)

    def buscar_cliente(self, id_cliente):
        return self.hash_table.buscar(id_cliente)

    def remover_cliente(self, id_cliente):
        return self.hash_table.remover(id_cliente)
