from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.settings import OPENAI_API_KEY

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

def dataset_description():
    """Descrição do dataset e suas colunas, com exemplos detalhados."""
    return """
O dataset contém as seguintes colunas, identificadas claramente como (Coluna), com exemplos para maior clareza:

1. REF_DATE (Coluna): Data de referência do registro.
   - Tipo: STRING (em formato ISO 8601).
   - Exemplo: "2017-06-01 00:00:00+00:00".

2. TARGET (Coluna): Alvo binário de inadimplência.
   - Tipo: INT.
   - Valores possíveis:
     - `1`: Mau pagador (inadimplência > 60 dias em 2 meses).
     - `0`: Bom pagador.
   - Exemplo: `1` ou `0`.

3. VAR2 (Coluna): Sexo do indivíduo.
   - Tipo: STRING.
   - Valores possíveis:
     - `M`: Masculino.
     - `F`: Feminino.
   - Exemplo: `M` ou `F`.

4. IDADE (Coluna): Idade do indivíduo em anos.
   - Tipo: FLOAT.
   - Exemplo: `34.137` (representando aproximadamente 34 anos e 50 dias).

5. VAR4 (Coluna): Flag de óbito.
   - Tipo: INT.
   - Valores possíveis:
     - `1`: Indivíduo faleceu.
     - `0`: Indivíduo está vivo.
   - Exemplo: `1` ou `0`.

6. VAR5 (Coluna): Unidade Federativa (UF) brasileira.
    - Também conhecida como estado ou estados. Qualquer menção a "estado" ou "estados" deve ser mapeada diretamente para esta coluna, `VAR5`.
    - Tipo: STRING.
    - Valores possíveis: Siglas de estados brasileiros (ex.: BA, PE, PB, RS).
    - Exemplo: PE (Pernambuco), SP (São Paulo).
    - **Nenhum apelido, como `UF`, deve ser usado; utilize apenas `VAR5`.**

7. VAR8 (Coluna): Classe social estimada.
   - Tipo: STRING.
   - Valores possíveis: Classificações qualitativas, representadas pelas categorias:
     - `A`: Classe social mais alta.
     - `B`: Classe social alta.
     - `C`: Classe social média.
     - `D`: Classe social baixa.
     - `E`: Classe social mais baixa.
   - Exemplos:
     - `D`: Representa uma classe social baixa.
     - `C`: Representa uma classe social média.

Observação Geral:
- **As queries devem operar exclusivamente nas colunas listadas acima, identificadas como (Coluna).**
- **Não substitua ou modifique os nomes das colunas; utilize-os exatamente como descritos.**
"""

def query_rules():
    """Regras para construção de queries."""
    return """
Regras para a query:
- Utilize exclusivamente as colunas identificadas como (Coluna) acima.
- Certifique-se de que o nome da tabela é "tabela".
- Use agregações (`AVG`, `SUM`, etc.) somente se solicitado explicitamente na pergunta.
- Se a pergunta incluir filtros (ex.: "apenas para estado = 'SP'"), adicione uma cláusula `WHERE` apropriada utilizando a coluna correspondente.
- Sempre agrupe os resultados (`GROUP BY`) quando necessário para cálculos agregados.
- Se solicitado um ordenamento (ex.: "em ordem decrescente"), adicione `ORDER BY`.
"""

def output_format():
    """Formato esperado para a saída."""
    return """
Formato esperado:
- Retorne apenas a query SQL, delimitada pelo bloco ```sql.
- Não inclua explicações adicionais ou comentários no retorno.
"""

def construct_system_message():
    """Constrói a mensagem do sistema unindo as partes das regras."""
    return f"""
Você é um assistente especializado em análise de dados SQL. Seu trabalho é converter perguntas feitas em linguagem natural em queries SQL que serão executadas em um dataset.

Aqui estão as informações importantes:
{dataset_description()}
{query_rules()}
{output_format()}
Agora, transforme a seguinte pergunta em uma query SQL:
"""

def generate_query(user_input):
    """Gera uma query SQL a partir da pergunta do usuário."""
    system_message_content = construct_system_message() + f'"{user_input}"'
    system_message = SystemMessage(content=system_message_content)
    human_message = HumanMessage(content=user_input)
    
    response = chat.invoke([system_message, human_message])
    return response.content
