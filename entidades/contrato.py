class Contrato:
    def __init__(self, id, corretor, cliente, imovel):
        self.id = id
        self.corretor = corretor
        self.cliente = cliente
        self.imovel = imovel

    def __str__(self):
        return f"Contrato(ID: {self.id}, Corretor: {self.corretor.nome}, Cliente: {self.cliente.nome}, Imóvel: {self.imovel.endereco})"
