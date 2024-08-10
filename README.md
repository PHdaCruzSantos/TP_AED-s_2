# Sistema Imobiliário - Projeto de Algoritmos e Estruturas de Dados

## Descrição do Projeto

Este projeto foi desenvolvido para o curso de Algoritmos e Estruturas de Dados com o objetivo de criar uma aplicação de gestão imobiliária. A aplicação permite armazenar, buscar, ordenar e alocar imóveis a clientes, gerenciados por corretores. A interface gráfica foi implementada em Python usando o Tkinter, e o projeto incorpora técnicas de busca sequencial e binária, além de ordenação de dados.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

📁/imobiliaria <br>
  |📄-- main.py <br>
📁 -- entidades/ <br>
  |📄-- imovel.py <br>
  |📄-- cliente.py <br>
  |📄-- corretor.py <br>
📁 -- funcionalidades/ <br>
  |📄-- busca.py <br>
  |📄-- ordenacao.py <br>
📁 -- sistema/ <br>
  |📄-- sistema_imobiliaria.py <br>
  |📄-- utils.py <br>
📁 -- logs/ <br>
  |📄-- busca_sequencial_log.txt <br>
  |📄-- busca_binaria_log.txt <br>
  |📄-- ordenacao_log.txt <br>

### Pastas e Arquivos

1. **`entidades/`**: Contém as classes `Imovel`, `Cliente` e `Corretor` que representam as entidades principais do sistema.
2. **`funcionalidades/`**: Inclui as funções de busca (`busca.py`) e ordenação (`ordenacao.py`).
3. **`sistema/`**: Contém o núcleo do sistema imobiliário (`sistema_imobiliaria.py`) e utilitários para geração de dados e registro de logs (`utils.py`).
4. **`logs/`**: Armazena os logs de execução das funções de busca e ordenação, separados em arquivos para cada tipo de operação.
5. **`main.py`**: Arquivo principal que inicia a aplicação e a interface gráfica.

## Funcionalidades Implementadas

### 1. Criação de Estruturas e Geração de Dados

- **Entidades**: Foram criadas as classes `Imovel`, `Cliente` e `Corretor` para representar as principais entidades do sistema.
- **Geração de Dados Desordenados**: Os dados de exemplo são gerados aleatoriamente e armazenados de forma desordenada. A função `gerar_imoveis`, por exemplo, cria uma lista de objetos `Imovel` que é embaralhada antes de ser salva.

### 2. Interface Gráfica com Tkinter

- **Busca Sequencial e Binária**: A interface permite que o usuário escolha entre busca sequencial e binária ao buscar imóveis, clientes e corretores.
- **Alocação de Imóveis**: Um imóvel pode ser alocado a um cliente por um corretor. A interface evita que um imóvel já alocado seja alocado novamente, mostrando uma mensagem de erro se isso for tentado.
- **Ordenação de Dados**: A interface inclui um botão para ordenar os dados de imóveis, clientes e corretores. Após a ordenação, os comboboxes são atualizados para refletir a nova ordem.

### 3. Registro de Logs

- **Logs de Execução**: O tempo de execução das buscas e da ordenação é registrado em arquivos de log separados:
  - `busca_sequencial_log.txt`
  - `busca_binaria_log.txt`
  - `ordenacao_log.txt`

### 4. Exibição de Imóveis Alocados

- A interface gráfica exibe uma lista de todos os imóveis que já foram alocados e quem são os clientes e corretores responsáveis por esses imóveis.

## Como Executar o Projeto

### Requisitos

- Python 3.x
- Tkinter (incluído na maioria das distribuições do Python)

### Passos para Executar

1. **Clonar o Repositório**

   - Clone o repositório do projeto para o seu computador.

2. **Executar o Script Principal**

   - Navegue até o diretório do projeto e execute o arquivo `main.py`:
     ```bash
     python main.py
     ```
   - Será solicitado o número de imóveis, clientes e corretores a serem gerados como dados de exemplo.

3. **Usar a Interface Gráfica**

   - A interface gráfica será exibida. Nela, você pode:
     - Selecionar entre busca sequencial e binária.
     - Alocar imóveis a clientes por meio de corretores.
     - Ordenar os dados.
     - Visualizar a lista de imóveis alocados.
   - A interface impede a alocação de um mesmo imóvel mais de uma vez.

4. **Verificar os Logs**
   - Os logs de execução das buscas e da ordenação podem ser encontrados na pasta `logs/`. Estes logs contêm informações sobre o tempo de execução das operações realizadas.

## Conclusão

Este projeto demonstra o uso de conceitos fundamentais de algoritmos e estruturas de dados, como busca, ordenação, e a importância de estruturas de dados bem definidas. A interface gráfica oferece uma maneira interativa de testar essas funcionalidades, enquanto os logs fornecem insights sobre o desempenho das operações.
