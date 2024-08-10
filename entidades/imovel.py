class Imovel:
    def __init__(self, id, endereco, preco, tipo, status):
        self.id = id
        self.endereco = endereco
        self.preco = preco
        self.tipo = tipo
        self.status = status

    def __str__(self):
        return f"Imovel(ID: {self.id}, Endereco: {self.endereco}, Preco: {self.preco}, Tipo: {self.tipo}, Status: {self.status})"
