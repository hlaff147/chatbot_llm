from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.settings import openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)


def dataset_description():
    """Descrição do dataset e suas colunas, com exemplos detalhados."""
    return """
O dataset contém as seguintes colunas, com exemplos para maior clareza:

1. REF_DATE: Data de referência do registro.
   - Tipo: STRING (em formato ISO 8601).
   - Exemplo: "2017-06-01 00:00:00+00:00".

2. TARGET: Alvo binário de inadimplência.
   - Tipo: INT.
   - Valores possíveis:
     - `1`: Mau pagador (inadimplência > 60 dias em 2 meses).
     - `0`: Bom pagador.
   - Exemplo: `1` ou `0`.

3. VAR2: Sexo do indivíduo.
   - Tipo: STRING.
   - Valores possíveis:
     - `M`: Masculino.
     - `F`: Feminino.
   - Exemplo: `M` ou `F`.

4. IDADE: Idade do indivíduo em anos.
   - Tipo: FLOAT.
   - Exemplo: `34.137` (representando aproximadamente 34 anos e 50 dias).

5. VAR4: Flag de óbito.
   - Tipo: INT.
   - Valores possíveis:
     - `1`: Indivíduo faleceu.
     - `0`: Indivíduo está vivo.
   - Exemplo: `1` ou `0`.

6. VAR5: Unidade Federativa (UF) brasileira.
   - Tipo: STRING.
   - Valores possíveis: Siglas de estados brasileiros (ex.: BA, PE, PB, RS).
   - Exemplo: `PE` (Pernambuco), `SP` (São Paulo).

7. VAR8: Classe social estimada.
   - Tipo: STRING.
   - Valores possíveis: Classificações qualitativas, como "Alta", "Média", "Baixa", "Altíssima".
   - Exemplo: `Alta` ou `Média`.

Observação Geral:
- As queries devem operar apenas nas colunas descritas acima.
- Nenhuma coluna ou tabela não listada deve ser utilizada.
"""

def query_rules():
    """Regras para construção de queries."""
    return """
Regras para a query:
- Sempre utilize apenas as colunas listadas acima.
- Certifique-se de que o nome da tabela é "tabela".
- Use agregações (`AVG`, `SUM`, etc.) somente se solicitado explicitamente na pergunta.
- Se a pergunta incluir filtros (ex.: "apenas para UF = 'SP'"), adicione uma cláusula `WHERE` apropriada.
- Sempre agrupe os resultados (`GROUP BY`) quando necessário para cálculos agregados.
- Se solicitado um ordenamento (ex.: "em ordem decrescente"), adicione `ORDER BY`.
"""

def output_format():
    """Formato esperado para a saída."""
    return """
Formato esperado:
- Retorne apenas a query SQL, delimitada pelo bloco ```sql.
- Não inclua explicações adicionais.
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
