import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from sistema.sistema_imobiliaria import SistemaImobiliaria
from sistema.utils import gerar_imoveis, gerar_clientes, gerar_corretores, salvar_dados
from funcionalidades.ordenacao import merge_sort
from funcionalidades.busca import buscar_sequencial, buscar_binaria

def criar_dados_exemplo(qtd_imoveis, qtd_clientes, qtd_corretores):
    imoveis = gerar_imoveis(qtd_imoveis)
    clientes = gerar_clientes(qtd_clientes)
    corretores = gerar_corretores(qtd_corretores)
    salvar_dados(imoveis, clientes, corretores)

class App:
    def __init__(self, root):
        self.sistema = SistemaImobiliaria()
        self.root = root
        self.root.title("Sistema Imobiliário")
        self.root.geometry("600x500")  # Ajuste de tamanho da interface
        self.create_widgets()

    def create_widgets(self):
        self.search_method_label = tk.Label(self.root, text="Método de Busca")
        self.search_method_label.pack()

        self.search_method = tk.StringVar(value="sequencial")
        self.sequencial_radio = tk.Radiobutton(self.root, text="Sequencial", variable=self.search_method, value="sequencial")
        self.binaria_radio = tk.Radiobutton(self.root, text="Binária", variable=self.search_method, value="binaria")
        self.sequencial_radio.pack()
        self.binaria_radio.pack()

        self.imovel_label = tk.Label(self.root, text="Selecionar Imóvel")
        self.imovel_label.pack()

        self.imovel_combobox = ttk.Combobox(self.root, values=[self._format_imovel(imovel) for imovel in self.sistema.imoveis])
        self.imovel_combobox.pack()

        self.cliente_label = tk.Label(self.root, text="Selecionar Cliente")
        self.cliente_label.pack()

        self.cliente_combobox = ttk.Combobox(self.root, values=[self._format_cliente(cliente) for cliente in self.sistema.clientes])
        self.cliente_combobox.pack()

        self.corretor_label = tk.Label(self.root, text="Selecionar Corretor")
        self.corretor_label.pack()

        self.corretor_combobox = ttk.Combobox(self.root, values=[corretor.id for corretor in self.sistema.corretores])
        self.corretor_combobox.pack()

        self.alocar_button = tk.Button(self.root, text="Alocar Imóvel", command=self.alocar_imovel)
        self.alocar_button.pack()

        self.ordenar_button = tk.Button(self.root, text="Ordenar Dados", command=self.ordenar_dados)
        self.ordenar_button.pack()

        self.lista_alocacoes_label = tk.Label(self.root, text="Imóveis Alocados")
        self.lista_alocacoes_label.pack()

        self.lista_alocacoes = tk.Text(self.root, height=10, width=50)
        self.lista_alocacoes.pack()

        self._atualizar_lista_alocacoes()

    def _format_imovel(self, imovel):
        alocacao = " (Alocado)" if imovel.status == "alocado" else ""
        return f"{imovel.id} - {imovel.endereco} - {imovel.preco} {alocacao}"

    def _format_cliente(self, cliente):
        imoveis_alocados = [imovel for imovel in self.sistema.imoveis if imovel.status == "alocado"]
        imoveis_cliente = [imovel.id for imovel in imoveis_alocados if cliente.id in [c.id for c in self.sistema.clientes]]
        alocacao = f" - Imóveis: {', '.join(imoveis_cliente)}" if imoveis_cliente else ""
        return f"{cliente.id} - {cliente.nome} {alocacao}"

    def alocar_imovel(self):
        id_imovel = self.imovel_combobox.get().split()[0]
        id_cliente = self.cliente_combobox.get().split()[0]
        id_corretor = self.corretor_combobox.get()

        if id_imovel and id_cliente and id_corretor:
            # Busca o imóvel, cliente e corretor usando o método selecionado
            imovel = self.buscar(self.sistema.imoveis, 'id', id_imovel)
            cliente = self.buscar(self.sistema.clientes, 'id', id_cliente)
            corretor = self.buscar(self.sistema.corretores, 'id', id_corretor)

            if imovel and cliente and corretor:
                if imovel.status == "disponível":
                    imovel.status = "alocado"
                    corretor.imoveis_gerenciados.append(imovel)
                    messagebox.showinfo("Sucesso", f"Imóvel {imovel.id} alocado ao cliente {cliente.id} pelo corretor {corretor.id}")
                    # Atualizar as listas após alocação
                    self.imovel_combobox['values'] = [self._format_imovel(im) for im in self.sistema.imoveis]
                    self._atualizar_lista_alocacoes()
                else:
                    messagebox.showwarning("Erro", "Este imóvel já está alocado!")
            else:
                messagebox.showwarning("Erro", "Erro ao localizar os dados para alocação!")
        else:
            messagebox.showwarning("Erro", "Por favor, selecione todas as opções!")

    def ordenar_dados(self):
        merge_sort(self.sistema.imoveis, 'id')
        merge_sort(self.sistema.clientes, 'id')
        merge_sort(self.sistema.corretores, 'id')
        messagebox.showinfo("Ordenação", "Os dados foram ordenados com sucesso!")
        # Atualizar as listas no combobox após ordenação
        self.imovel_combobox['values'] = [self._format_imovel(imovel) for imovel in self.sistema.imoveis]
        self.cliente_combobox['values'] = [self._format_cliente(cliente) for cliente in self.sistema.clientes]
        self.corretor_combobox['values'] = [corretor.id for corretor in self.sistema.corretores]

    def buscar(self, lista, chave, valor):
        if self.search_method.get() == "sequencial":
            return buscar_sequencial(lista, chave, valor)
        else:
            return buscar_binaria(lista, chave, valor)

    def _atualizar_lista_alocacoes(self):
        self.lista_alocacoes.delete(1.0, tk.END)
        for imovel in self.sistema.imoveis:
            if imovel.status == "alocado":
                self.lista_alocacoes.insert(tk.END, f"Imóvel {imovel.id} --> {imovel.status}.\n")

if __name__ == '__main__':
    qtd_imoveis = 50 #int(input("Quantidade de imóveis a gerar: "))
    qtd_clientes = 80 #int(input("Quantidade de clientes a gerar: "))
    qtd_corretores = 11 #int(input("Quantidade de corretores a gerar: "))

    criar_dados_exemplo(qtd_imoveis, qtd_clientes, qtd_corretores)

    root = tk.Tk()
    app = App(root)
    root.mainloop()
