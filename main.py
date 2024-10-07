import tkinter as tk
from tkinter import ttk, messagebox
import time
from sistema.sistema_imobiliaria import SistemaImobiliaria
from sistema.utils import gerar_imoveis, gerar_clientes, gerar_corretores, salvar_dados, log_time_sequencial, log_time_binaria
from funcionalidades.ordenacao import merge_sort
from funcionalidades.busca import buscar_sequencial, buscar_binaria
from funcionalidades.tabela_hash import HashTable
from entidades.cliente import Cliente

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

        # Configuração do Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.hash_table = HashTable("db/clientes.db")
        self.carregar_clientes_para_hash()

        # Criar as abas
        self.create_main_tab()  # Aba principal
        self.create_client_hash_tab()  # Aba de Tabela Hash para clientes

    def create_main_tab(self):
        # Frame principal para a aba do sistema imobiliário
        main_frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        self.notebook.add(main_frame, text="Sistema Imobiliário")

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

        # Seção de Imóveis
        selecao_frame = ttk.LabelFrame(main_frame, text="Selecionar Dados", padding="10 10 10 10")
        selecao_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        self.imovel_label = ttk.Label(selecao_frame, text="Selecionar Imóvel:")
        self.imovel_label.grid(row=0, column=0, sticky=tk.W)

        self.imovel_combobox = ttk.Combobox(selecao_frame, values=[self._format_imovel(imovel) for imovel in self.sistema.imoveis])
        self.imovel_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.cliente_label = ttk.Label(selecao_frame, text="Selecionar Cliente:")
        self.cliente_label.grid(row=1, column=0, sticky=tk.W)

        self.cliente_combobox = ttk.Combobox(selecao_frame, values=[self._format_cliente(cliente) for cliente in self.sistema.clientes])
        self.cliente_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.corretor_label = ttk.Label(selecao_frame, text="Selecionar Corretor:")
        self.corretor_label.grid(row=2, column=0, sticky=tk.W)

        self.corretor_combobox = ttk.Combobox(selecao_frame, values=[corretor.id for corretor in self.sistema.corretores])
        self.corretor_combobox.grid(row=2, column=1, padx=10, pady=5)

        # Agrupamento das ações
        acoes_frame = ttk.LabelFrame(main_frame, text="Ações Disponíveis", padding="10 10 10 10")
        acoes_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 10))

        self.alocar_button = ttk.Button(acoes_frame, text="Alocar Imóvel", command=self.alocar_imovel, style='BlackTextButton.TButton')
        self.alocar_button.grid(row=0, column=0, padx=10, pady=10)

        self.ordenar_button = ttk.Button(acoes_frame, text="Ordenar Dados (Merge Sort)", command=self.ordenar_dados, style='BlackTextButton.TButton')
        self.ordenar_button.grid(row=0, column=1, padx=10, pady=10)

        self.ordenar_substituicao_button = ttk.Button(acoes_frame, text="Ordenar por Seleção por Substituição", command=self.ordenar_substituicao, style='BlackTextButton.TButton')
        self.ordenar_substituicao_button.grid(row=0, column=2, padx=10, pady=10)

        # Lista de Imóveis Alocados
        self.lista_alocacoes_label = ttk.Label(main_frame, text="Imóveis Alocados:")
        self.lista_alocacoes_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))

        self.lista_alocacoes = tk.Text(main_frame, height=10, width=70, font=('Arial', 10))
        self.lista_alocacoes.grid(row=4, column=0, padx=10, pady=(5, 10))

        self._atualizar_lista_alocacoes()

    def create_client_hash_tab(self):
        # Frame para a aba de Clientes usando Tabela Hash
        hash_frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        self.notebook.add(hash_frame, text="Clientes (Hash)")

        # Label para instruções
        hash_label = ttk.Label(hash_frame, text="Gerenciamento de Clientes com Hash:", font=('Arial', 12))
        hash_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Campo de ID do cliente
        self.label_id_cliente = ttk.Label(hash_frame, text="ID do Cliente:")
        self.label_id_cliente.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.entry_id_cliente = ttk.Entry(hash_frame)
        self.entry_id_cliente.grid(row=1, column=1, padx=5, pady=5)

        # Campo de Nome do cliente
        self.label_nome_cliente = ttk.Label(hash_frame, text="Nome do Cliente:")
        self.label_nome_cliente.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.entry_nome_cliente = ttk.Entry(hash_frame)
        self.entry_nome_cliente.grid(row=2, column=1, padx=5, pady=5)

        # Campo de Telefone do cliente
        self.label_telefone_cliente = ttk.Label(hash_frame, text="Telefone do Cliente:")
        self.label_telefone_cliente.grid(row=3, column=0, sticky=tk.W, padx=5)
        self.entry_telefone_cliente = ttk.Entry(hash_frame)
        self.entry_telefone_cliente.grid(row=3, column=1, padx=5, pady=5)

        # Campo de E-mail do cliente
        self.label_email_cliente = ttk.Label(hash_frame, text="E-mail do Cliente:")
        self.label_email_cliente.grid(row=4, column=0, sticky=tk.W, padx=5)
        self.entry_email_cliente = ttk.Entry(hash_frame)
        self.entry_email_cliente.grid(row=4, column=1, padx=5, pady=5)

        # Campo de Iinteresse do cliente
        self.label_interesse_cliente = ttk.Label(hash_frame, text="Interesse do Cliente:")
        self.label_interesse_cliente.grid(row=5, column=0, sticky=tk.W, padx=5)
        self.entry_interesse_cliente = ttk.Entry(hash_frame)
        self.entry_interesse_cliente.grid(row=5, column=1, padx=5, pady=5)

        # Botão para adicionar cliente
        self.btn_inserir_cliente = ttk.Button(hash_frame, text="Adicionar Cliente", command=self.inserir_cliente)
        self.btn_inserir_cliente.grid(row=3, column=0, padx=10, pady=10)

        # Botão para buscar cliente
        self.btn_buscar_cliente = ttk.Button(hash_frame, text="Buscar Cliente", command=self.buscar_cliente)
        self.btn_buscar_cliente.grid(row=3, column=1, padx=10, pady=10)

        # Botão para remover cliente
        self.btn_remover_cliente = ttk.Button(hash_frame, text="Remover Cliente", command=self.remover_cliente)
        self.btn_remover_cliente.grid(row=3, column=2, padx=10, pady=10)

        # Campo de texto para mostrar o resultado das operações
        self.resultado_texto = tk.Text(hash_frame, height=10, width=70, font=('Arial', 10))
        self.resultado_texto.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        for cliente in self.sistema.clientes:
            self.sistema.inserir_cliente(cliente.id, cliente.nome, cliente.telefone, cliente.email, cliente.interesse)


    def carregar_clientes_para_hash(self):
        """
        Carrega os clientes existentes na tabela hash.
        """
        for cliente in self.sistema.clientes:
            self.hash_table.inserir(cliente)

    def inserir_cliente(self):
        id_cliente = int(self.entry_id_cliente.get())
        nome_cliente = self.entry_nome_cliente.get()
        telefone_cliente = self.entry_telefone_cliente.get()
        email_cliente = self.entry_email_cliente.get()
        interesse_cliente = self.entry_interesse_cliente.get()
        self.sistema.inserir_cliente(id_cliente, nome_cliente, telefone_cliente, email_cliente, interesse_cliente)
        self.resultado_texto.insert(tk.END, f"Cliente {nome_cliente} inserido com sucesso!\n")


    def buscar_cliente(self):
        id_cliente = int(self.entry_id_cliente.get())
        cliente = self.sistema.buscar_cliente(id_cliente)
        self.resultado_texto.delete(1.0, tk.END)
        if cliente:
            self.resultado_texto.insert(tk.END, f"Cliente encontrado: {cliente.nome}\n")
        else:
            self.resultado_texto.insert(tk.END, f"Cliente {id_cliente} não encontrado.\n")


    def remover_cliente(self):
        id_cliente = int(self.entry_id_cliente.get())
        if self.sistema.remover_cliente(id_cliente):
            self.resultado_texto.insert(tk.END, f"Cliente {id_cliente} removido com sucesso.\n")
        else:
            self.resultado_texto.insert(tk.END, f"Cliente {id_cliente} não encontrado.\n")


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
            imovel = self.buscar(self.sistema.imoveis, 'id', id_imovel)
            cliente = self.buscar(self.sistema.clientes, 'id', id_cliente)
            corretor = self.buscar(self.sistema.corretores, 'id', id_corretor)

            if imovel and cliente and corretor:
                if imovel.status == "disponível":
                    imovel.status = "alocado"
                    corretor.imoveis_gerenciados.append(imovel)
                    messagebox.showinfo("Sucesso", f"Imóvel {imovel.id} alocado ao cliente {cliente.id} pelo corretor {corretor.id}")
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
        self.imovel_combobox['values'] = [self._format_imovel(imovel) for imovel in self.sistema.imoveis]
        self.cliente_combobox['values'] = [self._format_cliente(cliente) for cliente in self.sistema.clientes]
        self.corretor_combobox['values'] = [corretor.id for corretor in self.sistema.corretores]

    def ordenar_substituicao(self):
        messagebox.showinfo("Ordenação", "Os dados estão sendo ordenados por Seleção por Substituição. Aguarde...")

        try:
            self.sistema.ordenar_arquivo_binario(self.sistema.imoveis, 100, 'imoveis')
            self.sistema.ordenar_arquivo_binario(self.sistema.clientes, 100, 'clientes')
            self.sistema.ordenar_arquivo_binario(self.sistema.corretores, 100, 'corretores')

            messagebox.showinfo("Ordenação", "Os dados foram ordenados por Seleção por Substituição com sucesso!")
            self.imovel_combobox['values'] = [self._format_imovel(imovel) for imovel in self.sistema.imoveis]
            self.cliente_combobox['values'] = [self._format_cliente(cliente) for cliente in self.sistema.clientes]
            self.corretor_combobox['values'] = [corretor.id for corretor in self.sistema.corretores]

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a ordenação: {str(e)}")
            print(e)

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
    qtd_corretores = 100    # int(input("Quantidade de corretores a gerar: "))

    criar_dados_exemplo(qtd_imoveis, qtd_clientes, qtd_corretores)

    root = tk.Tk()
    app = App(root)
    root.mainloop()
