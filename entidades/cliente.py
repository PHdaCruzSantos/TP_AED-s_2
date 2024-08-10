class Cliente:
    def __init__(self, id, nome, telefone, email, interesse):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.interesse = interesse

    def __str__(self):
        return f"Cliente(ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Email: {self.email})"
