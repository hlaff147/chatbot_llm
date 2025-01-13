
---

# Chatbot de Análise de Dados com LLMs

Este é um projeto **WIP (Work In Progress)** que implementa um chatbot para análise de dados utilizando **Streamlit**, **Pandas**, **DuckDB** e **LLMs (Large Language Models)**. O objetivo é interpretar perguntas feitas em linguagem natural, convertê-las em queries SQL, executar essas queries em um banco de dados local (ou futuramente na nuvem), e retornar insights significativos de maneira clara e explicativa.

---

## 🚀 Funcionalidades

- **Conversão de Linguagem Natural para SQL**: Perguntas feitas em linguagem natural são convertidas em queries SQL utilizando modelos de linguagem.
- **Validação de Perguntas e Queries**:
  - Garantia de aderência às regras de negócio e esquema do banco.
  - Verificação de sintaxe SQL para evitar erros comuns.
- **Execução Local**:
  - Integração com **DuckDB** para executar queries localmente no dataset fornecido.
- **Interface Intuitiva**:
  - Desenvolvido com **Streamlit**, permitindo interação simples e amigável.
- **Respostas Explicativas**:
  - Os resultados das queries são analisados e apresentados de forma clara e detalhada.

---

## 📂 Estrutura do Projeto

```plaintext
project/
├── main.py               # Código principal (integração Streamlit)
├── config/
│   └── settings.py       # Configurações do projeto (ex.: caminho do dataset)
├── models/
│   ├── query_generator.py           # Geração de queries SQL
│   ├── input_validator.py           # Validação de entrada do usuário
│   ├── analyse_query_response.py    # Análise dos resultados da query
│   ├── query_validator.py           # Validação sintática e de negócio das queries
├── utils/
│   ├── executor_duck.py             # Execução de queries com DuckDB
│   ├── sql_extractor.py             # Extração de SQL a partir da resposta do GPT
├── data/
│   └── dataset.csv                  # Dataset utilizado pelo chatbot
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- **Frameworks e Ferramentas**:
  - [Streamlit](https://streamlit.io/): Interface do chatbot.
  - [DuckDB](https://duckdb.org/): Execução local de queries SQL.
  - [Pandas](https://pandas.pydata.org/): Processamento e manipulação de dados.
  - [OpenAI GPT](https://openai.com/): Conversão de linguagem natural para SQL.
  
- **Integração com LLM**:
  - Modelos como OpenAI GPT para geração de queries e análise.

---

## 📝 Esquema do Banco de Dados

O chatbot utiliza um dataset que contém as seguintes colunas (não são permitidas consultas fora deste esquema):

| Coluna      | Descrição                                                                                  |
|-------------|--------------------------------------------------------------------------------------------|
| `REF_DATE`  | Data de referência do registro.                                                           |
| `TARGET`    | Alvo binário de inadimplência (1: Mau Pagador, atraso > 60 dias em 2 meses).               |
| `VAR2`      | Sexo do indivíduo (masculino/feminino).                                                   |
| `IDADE`     | Idade do indivíduo.                                                                       |
| `VAR4`      | Flag de óbito (indica se o indivíduo faleceu).                                             |
| `VAR5`      | Unidade Federativa (UF) brasileira.                                                       |
| `VAR8`      | Classe social estimada.                                                                   |

---

## 🛠️ Como Executar

### Pré-requisitos

1. Python 3.8 ou superior.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Executar o Chatbot

1. Carregue o dataset em `data/dataset.csv` (ou configure o caminho em `config/settings.py`).
2. Inicie o Streamlit:
   ```bash
   streamlit run main.py
   ```
3. Acesse a interface no navegador (geralmente em `http://localhost:8501`).

---

## 🛡️ Validações Implementadas

- **Validação de Perguntas**:
  - Garante que o input do usuário está de acordo com o esquema do banco.
- **Validação de Queries SQL**:
  - Verifica sintaxe SQL.
  - Valida aderência às regras de negócio, como uso correto das colunas e funções.

---

## 📌 Próximos Passos

- **Integração com AWS**:
  - Utilizar **Boto3** e **Athena** para executar queries na nuvem.
- **Melhorias na Análise**:
  - Adicionar insights gráficos com **Plotly** ou **Matplotlib**.
- **Suporte a Consultas Complexas**:
  - Habilitar filtros mais avançados com múltiplos critérios.

---
