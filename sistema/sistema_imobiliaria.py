import pickle
from funcionalidades.busca import buscar_sequencial
from entidades.imovel import Imovel
from entidades.cliente import Cliente
from entidades.corretor import Corretor

class SistemaImobiliaria:
    def __init__(self):
        with open('imoveis.db', 'rb') as f:
            self.imoveis = pickle.load(f)
        with open('clientes.db', 'rb') as f:
            self.clientes = pickle.load(f)
        with open('corretores.db', 'rb') as f:
            self.corretores = pickle.load(f)

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
