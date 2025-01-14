from config.settings import openai_api_key
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

def construct_validation_message():
    """
    Constrói o prompt para validação de sintaxe e segurança da query SQL.
    """
    return "\n".join([
        get_intro_message(),
        get_syntax_rules_message(),
        get_response_format_message()
    ])

def get_intro_message():
    """
    Retorna a introdução do prompt.
    """
    return (
        "Você é um assistente especializado em validação de queries SQL. "
        "Sua tarefa é verificar se a query SQL fornecida é sintaticamente correta "
        "e não apresenta riscos de segurança, como operações proibidas."
    )

def get_syntax_rules_message():
    """
    Retorna as regras para validação sintática e de segurança.
    """
    return (
        "Regras de validação:\n"
        "1. Verifique os seguintes problemas comuns:\n"
        "   - Uso de `NOT IN` com valores NULL.\n"
        "   - Uso de `UNION` quando `UNION ALL` deveria ser usado.\n"
        "   - Uso de `BETWEEN` para intervalos exclusivos.\n"
        "   - Mismatch de tipo de dados em predicados.\n"
        "   - Identificadores não citados corretamente.\n"
        "   - Número incorreto de argumentos para funções.\n"
        "   - Cast para o tipo de dados incorreto.\n"
        "   - Uso inadequado de colunas em joins.\n"
        "2. Bloqueie queries que contenham as seguintes palavras-chave:\n"
        "   - INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE.\n"
    )

def get_response_format_message():
    """
    Retorna o formato esperado da resposta.
    """
    return (
        "Formato esperado:\n"
        "- Se a query for válida, responda: 'Válida: A query está correta.'\n"
        "- Se a query for inválida, responda: 'Inválida: [Explique o problema encontrado].'\n"
        "- Não forneça explicações adicionais ou corrija a query."
    )

def contains_prohibited_keywords(query):
    """
    Verifica se a query contém palavras-chave proibidas.
    """
    prohibited_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"]
    for keyword in prohibited_keywords:
        if keyword in query.upper():
            return True
    return False

def validate_query_syntax(query_sql):
    """
    Valida a sintaxe e a segurança de uma query SQL.
    """
    try:
        if contains_prohibited_keywords(query_sql):
            return {
                "valido": False,
                "racional": "Inválida: A query contém operações proibidas, como INSERT, UPDATE, DELETE, ou ALTER."
            }

        system_message_content = construct_validation_message()
        system_message = SystemMessage(content=system_message_content)
        human_message = HumanMessage(content=query_sql)

        response = chat.invoke([system_message, human_message])

        content = response.content.strip()
        if content.startswith("Válida"):
            return {
                "valido": True,
                "racional": content
            }
        else:
            return {
                "valido": False,
                "racional": content
            }
    except Exception as e:
        return {
            "valido": False,
            "racional": f"Erro ao validar a query: {str(e)}"
        }
