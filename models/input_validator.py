from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.settings import openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key,model_kwargs={"response_format": {"type": "json_object"}})

def construct_validation_message():
    """
    Constrói a mensagem do sistema para validar a pergunta do usuário.
    """
    return """
Você é um assistente especializado em validação de entradas para um sistema de análise de dados SQL.
Seu trabalho é verificar se a pergunta feita pelo usuário está de acordo com o esquema do banco de dados.

Especificações importantes:
1. O banco de dados contém apenas as seguintes colunas:
   - REF_DATE: Data de referência do registro.
   - TARGET: Alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses).
   - VAR2: Sexo do indivíduo (masculino/feminino).
   - IDADE: Idade do indivíduo.
   - VAR4: Flag de óbito (indica se o indivíduo faleceu).
   - VAR5: Unidade federativa (UF) brasileira.
   - VAR8: Classe social estimada.

2. Regras de validação:
   - A pergunta deve usar apenas as colunas disponíveis listadas acima.
   - A pergunta não pode fazer referência a colunas inexistentes.
   - A pergunta deve ser clara e permitir a geração de uma query SQL válida.

Formato da resposta (JSON) primeiro explique seu racional e depois indique se é ou nao uma pergunta válida:
  {
    racional:str,
    valido:bool,
  }
"""


def validate_user_input(user_input):
    """
    Valida se o input do usuário está conforme o esquema do banco.
    """
    system_message_content = construct_validation_message()
    system_message = SystemMessage(content=system_message_content)
    
    human_message = HumanMessage(content=user_input)
    
    response = chat.invoke([system_message, human_message])
    return response.content
