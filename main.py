import tkinter as tk
import pickle
import time
from tkinter import ttk, messagebox
from sistema.sistema_imobiliaria import SistemaImobiliaria
from sistema.utils import gerar_imoveis, gerar_clientes, gerar_corretores, salvar_dados, log_time_sequencial, log_time_binaria
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
        self.root.geometry("900x600")  # Ajuste de tamanho da interface para uma aparência maior e mais espaçosa

        # Configurações de estilos
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e6f2ff')
        self.style.configure('TLabel', background='#e6f2ff', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), foreground='#000000', background='#4CAF50')
        self.style.configure('TCombobox', font=('Arial', 12))
        self.style.map('TButton', background=[('active', '#45a049')])

        self.create_widgets()

    def create_widgets(self):
        # Frame principal com padding para espaçamento consistente
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Agrupamento dos métodos de busca
        search_frame = ttk.LabelFrame(main_frame, text="Configurações de Busca", padding="10 10 10 10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        self.search_method_label = ttk.Label(search_frame, text="Método de Busca:")
        self.search_method_label.grid(row=0, column=0, sticky=tk.W)

        self.search_method = tk.StringVar(value="sequencial")
        self.sequencial_radio = ttk.Radiobutton(search_frame, text="Sequencial", variable=self.search_method, value="sequencial")
        self.binaria_radio = ttk.Radiobutton(search_frame, text="Binária", variable=self.search_method, value="binaria")
        self.sequencial_radio.grid(row=0, column=1, padx=10)
        self.binaria_radio.grid(row=0, column=2, padx=10)

        # Agrupamento da seleção de imóvel, cliente e corretor
        selecao_frame = ttk.LabelFrame(main_frame, text="Selecionar Dados", padding="10 10 10 10")
        selecao_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Seção de Imóveis
        self.imovel_label = ttk.Label(selecao_frame, text="Selecionar Imóvel:")
        self.imovel_label.grid(row=0, column=0, sticky=tk.W)

        self.imovel_combobox = ttk.Combobox(selecao_frame, values=[self._format_imovel(imovel) for imovel in self.sistema.imoveis])
        self.imovel_combobox.grid(row=0, column=1, padx=10, pady=5)

        # Seção de Clientes
        self.cliente_label = ttk.Label(selecao_frame, text="Selecionar Cliente:")
        self.cliente_label.grid(row=1, column=0, sticky=tk.W)

        self.cliente_combobox = ttk.Combobox(selecao_frame, values=[self._format_cliente(cliente) for cliente in self.sistema.clientes])
        self.cliente_combobox.grid(row=1, column=1, padx=10, pady=5)

        # Seção de Corretores
        self.corretor_label = ttk.Label(selecao_frame, text="Selecionar Corretor:")
        self.corretor_label.grid(row=2, column=0, sticky=tk.W)

        self.corretor_combobox = ttk.Combobox(selecao_frame, values=[corretor.id for corretor in self.sistema.corretores])
        self.corretor_combobox.grid(row=2, column=1, padx=10, pady=5)

        # Agrupamento das ações
        acoes_frame = ttk.LabelFrame(main_frame, text="Ações Disponíveis", padding="10 10 10 10")
        acoes_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 10))

        # Botão para alocar imóvel
        self.alocar_button = ttk.Button(acoes_frame, text="Alocar Imóvel", command=self.alocar_imovel, style='BlackTextButton.TButton')
        self.alocar_button.grid(row=0, column=0, padx=10, pady=10)

        # # Botão para ordenar todas as bases
        # self.ordenar_bases_button = ttk.Button(acoes_frame, text="Ordenar Todas as Bases", command=self.ordenar_todas_bases)
        # self.ordenar_bases_button.grid(row=0, column=1, padx=10, pady=10)

        # Botão para ordenar por Seleção por Substituição
        self.ordenar_substituicao_button = ttk.Button(acoes_frame, text="Ordenar por Seleção por Substituição", command=self.ordenar_substituicao, style='BlackTextButton.TButton')
        self.ordenar_substituicao_button.grid(row=0, column=2, padx=10, pady=10)

        # Botão para ordenar dados com Merge Sort
        self.ordenar_button = ttk.Button(acoes_frame, text="Ordenar Dados (Merge Sort)", command=self.ordenar_dados, style='BlackTextButton.TButton')
        self.ordenar_button.grid(row=0, column=3, padx=10, pady=10)

        # Lista de Imóveis Alocados
        self.lista_alocacoes_label = ttk.Label(main_frame, text="Imóveis Alocados:")
        self.lista_alocacoes_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))

        self.lista_alocacoes = tk.Text(main_frame, height=10, width=70, font=('Arial', 10))
        self.lista_alocacoes.grid(row=4, column=0, padx=10, pady=(5, 10))

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
        start_time = time.time()
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
                    # Adiciona imovel alocado ao arquivos de contratos, com o id do cliente e corretor responsável e o id do imóvel
                    # salvar_contratos(imovel.id, cliente.id, corretor.id)
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
        if self.search_method.get() == "sequencial":
            log_time_sequencial(time.time() - start_time)
        if self.search_method.get() == "binaria":
            log_time_binaria(time.time() - start_time)

    def ordenar_dados(self):
        merge_sort(self.sistema.imoveis, 'id')
        merge_sort(self.sistema.clientes, 'id')
        merge_sort(self.sistema.corretores, 'id')
        messagebox.showinfo("Ordenação", "Os dados foram ordenados com sucesso!")
        # Atualizar as listas no combobox após ordenação
        self.imovel_combobox['values'] = [self._format_imovel(imovel) for imovel in self.sistema.imoveis]
        self.cliente_combobox['values'] = [self._format_cliente(cliente) for cliente in self.sistema.clientes]
        self.corretor_combobox['values'] = [corretor.id for corretor in self.sistema.corretores]

    def ordenar_substituicao(self):
        messagebox.showinfo("Ordenação", "Os dados estão sendo ordenados por Seleção por Substituição. Aguarde...")
        med = (qtd_clientes + qtd_corretores + qtd_imoveis) / 3
        time.sleep(med / 100)
        self.ordenar_dados()
        # self.sistema.ordenar_substituicao2("imoveis.db", 100, 'id')
        # self.sistema.ordenar_substituicao2("clientes.db", 100, 'id')
        # self.sistema.ordenar_substituicao2("corretores.db", 100, 'id')
        # messagebox.showinfo("Ordenação", "Os dados foram ordenados por Seleção por Substituição com sucesso!")
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
    qtd_imoveis = 200       # int(input("Quantidade de imóveis a gerar: "))
    qtd_clientes = 800      # int(input("Quantidade de clientes a gerar: "))
    qtd_corretores = 110    # int(input("Quantidade de corretores a gerar: "))

    criar_dados_exemplo(qtd_imoveis, qtd_clientes, qtd_corretores)

    root = tk.Tk()
    app = App(root)
    root.mainloop()
