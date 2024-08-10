class Corretor:
    def __init__(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.imoveis_gerenciados = []

    def __str__(self):
        return f"Corretor(ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Email: {self.email})"
