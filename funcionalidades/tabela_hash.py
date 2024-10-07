import os
import pickle
from entidades.cliente import Cliente

class HashTable:
    def __init__(self, base_path):
        self.table = {}
        self.base_path = base_path
        self.load_base()

    def load_base(self):
        if os.path.exists(self.base_path):
            with open(self.base_path, 'rb') as f:
                try:
                    while True:
                        cliente = pickle.load(f)
                        if isinstance(cliente, Cliente):
                            self.table[cliente.id] = cliente
                except EOFError:
                    pass

    def save_base(self):
        # Verificar se o diretório existe, caso contrário, criar
        directory = os.path.dirname(self.base_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(self.base_path, 'wb') as f:
            for cliente in self.table.values():
                pickle.dump(cliente, f)

    def inserir(self, cliente):
        self.table[cliente.id] = cliente
        self.save_base()

    def buscar(self, id_cliente):
        return self.table.get(id_cliente, None)

    def remover(self, id_cliente):
        if id_cliente in self.table:
            del self.table[id_cliente]
            self.save_base()
            return True
        return False