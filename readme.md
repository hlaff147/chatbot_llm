
---

# Chatbot de Análise de Dados com LLMs

Este é um projeto **WIP (Work In Progress)** que implementa um chatbot para análise de dados utilizando **Streamlit**, **Pandas**, **DuckDB**, **AWS Athena**, **Boto3**, e **LLMs (Large Language Models)**. O objetivo é interpretar perguntas feitas em linguagem natural, convertê-las em queries SQL, executar essas queries em um banco de dados local ou na nuvem, e retornar insights significativos de maneira clara e explicativa.

---

## 🚀 Funcionalidades

- **Conversão de Linguagem Natural para SQL**: Perguntas feitas em linguagem natural são convertidas em queries SQL utilizando modelos de linguagem.
- **Validação de Perguntas e Queries**:
  - Verificação de sintaxe SQL e segurança da query.
  - Bloqueio de operações de modificação do banco (ex.: `INSERT`, `UPDATE`, `DELETE`).
- **Execução Local e em Nuvem**:
  - Integração com **DuckDB** para execução local de queries.
  - Integração com **AWS Athena** para execução de queries na nuvem.
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
│   └── settings.py       # Configurações do projeto (ex.: caminho do dataset, credenciais AWS)
├── models/
│   ├── query_generator.py           # Geração de queries SQL
│   ├── input_validator.py           # Validação de entrada do usuário
│   ├── analyse_query_response.py    # Análise dos resultados da query
│   ├── query_sql_validator.py       # Validação sintática das queries SQL
├── utils/
│   ├── executor_duck.py             # Execução de queries com DuckDB
│   ├── executor_athena.py           # Execução de queries com AWS Athena
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
  - [AWS Athena](https://aws.amazon.com/athena/): Execução de queries SQL na nuvem.
  - [Boto3](https://boto3.amazonaws.com/): Integração com serviços AWS.
  - [OpenAI GPT](https://openai.com/): Conversão de linguagem natural para SQL.
  
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

1. **Python 3.8** ou superior.
2. **AWS CLI** configurado com acesso válido.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração do Ambiente

1. Configure as credenciais AWS em `~/.aws/credentials` ou diretamente no código (via `settings.py`).
2. Certifique-se de que o dataset `dataset.csv` está em `data/` ou altere o caminho no arquivo `settings.py`.

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
  - Garante que o input do usuário é coerente e seguro.
- **Validação de Queries SQL**:
  - Verifica sintaxe SQL e bloqueia operações potencialmente destrutivas (`INSERT`, `UPDATE`, etc.).

---

## 📌 Próximos Passos

- **Melhorias na Análise**:
  - Adicionar gráficos e visualizações com **Plotly** ou **Matplotlib**.
- **Otimização de Performance**:
  - Implementar cache para evitar execução repetitiva de queries já realizadas.

---
