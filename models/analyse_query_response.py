from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config.settings import OPENAI_API_KEY
from config.logging_config import logger  # Importa o logger configurado

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

def construct_analysis_message():
    """
    Constrói a mensagem do sistema para analisar o resultado da query.
    """
    logger.debug("Construindo a mensagem do sistema para análise.")
    return """
Você é um assistente especializado em análise de dados SQL. Sua tarefa é analisar os resultados de uma query SQL e apresentar uma resposta explicativa, clara e enfatizando os pontos mais importantes.

Especificações:
1. Considere que o banco de dados contém as seguintes colunas:
   - REF_DATE: Data de referência do registro.
   - TARGET: Alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses).
   - VAR2: Sexo do indivíduo (masculino/feminino).
   - IDADE: Idade do indivíduo.
   - VAR4: Flag de óbito (indica se o indivíduo faleceu).
   - VAR5: Unidade federativa (UF) brasileira.
   - VAR8: Classe social estimada.

2. Ao interpretar o resultado:
   - Destaque tendências ou insights importantes (ex.: inadimplência alta em determinadas UFs, diferenças significativas por classe social).
   - Use uma linguagem simples e objetiva, explicando o que os números significam para um usuário leigo.
   - Se houver discrepâncias ou padrões inesperados, mencione isso como um ponto de atenção.

Formato esperado:
- Forneça um parágrafo explicativo.
- Inclua sugestões ou possíveis implicações, se aplicável.
"""

def analyse_response_query(query_result):
    """
    Gera uma resposta explicativa a partir do resultado da query.
    """
    logger.info("Iniciando análise do resultado da query.")
    try:
        # Log do resultado da query
        logger.debug(f"Resultado da query recebido: {query_result}")
        
        system_message_content = construct_analysis_message() + f"\nAqui está o resultado da query em formato tabular:\n{query_result}"
        system_message = SystemMessage(content=system_message_content)
        
        # Log do conteúdo da mensagem do sistema
        logger.debug(f"Mensagem do sistema construída: {system_message.content}")
        
        response = chat.invoke([system_message])
        
        logger.info("Análise concluída com sucesso.")
        logger.debug(f"Resposta gerada pelo modelo: {response.content}")
        
        return {
            "resultado_query": query_result,
            "analise": response.content
        }
    except Exception as e:
        logger.error(f"Erro ao analisar o resultado da query: {e}")
        return {
            "resultado_query": query_result,
            "erro": f"Erro ao analisar o resultado da query: {e}"
        }
