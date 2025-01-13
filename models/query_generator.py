from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.settings import openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)


def dataset_description():
    """Descrição do dataset e suas colunas."""
    return """
O dataset contém as seguintes colunas:
- REF_DATE: Data de referência do registro.
- TARGET: Alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses).
- VAR2: Sexo do indivíduo (masculino/feminino).
- IDADE: Idade do indivíduo.
- VAR4: Flag de óbito (indica se o indivíduo faleceu).
- VAR5: Unidade federativa (UF) brasileira.
- VAR8: Classe social estimada.
"""

def query_rules():
    """Regras para construção de queries."""
    return """
Regras para a query:
- Sempre utilize apenas as colunas listadas acima.
- Certifique-se de que o nome da tabela é "tabela" (substituída posteriormente no código).
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
