from config.settings import openai_api_key
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Inicializar o modelo de chat
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

def construct_validation_message():
    """
    Constrói o prompt completo para validação da query SQL.
    """
    return "\n".join([
        get_intro_message(),
        get_schema_message(),
        get_business_rules_message(),
        get_syntax_rules_message(),
        get_response_format_message()
    ])
    
def get_intro_message():
    """
    Retorna a introdução do prompt.
    """
    return """
Você é um assistente especializado em validação de queries SQL. Sua tarefa é validar a query SQL fornecida para identificar possíveis erros e garantir que ela esteja correta tanto do ponto de vista técnico quanto de negócios.
"""

def get_schema_message():
    """
    Retorna a descrição do esquema do banco de dados.
    """
    return """
Especificações do esquema:
- O banco de dados contém as seguintes colunas (nenhuma query deve utilizar informações de outras colunas):
  - REF_DATE: Data de referência do registro.
  - TARGET: Alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses).
  - VAR2: Sexo do indivíduo (masculino/feminino).
  - IDADE: Idade do indivíduo.
  - VAR4: Flag de óbito (indica se o indivíduo faleceu).
  - VAR5: Unidade federativa (UF) brasileira.
  - VAR8: Classe social estimada.
"""

def get_business_rules_message():
    """
    Retorna as regras de negócio para validação.
    """
    return """
Regras de validação de negócio:
1. A query deve utilizar apenas as colunas listadas acima.
2. Nenhuma query deve referenciar tabelas ou colunas inexistentes.
3. O uso de `TARGET` deve ser consistente com sua definição como um indicador binário de inadimplência.
   - Exemplo: Calcular inadimplência média (AVG(TARGET)) para grupos específicos.
4. O uso de `VAR4` deve verificar explicitamente valores binários.
   - Exemplo: `WHERE VAR4 = 1` para registros onde o indivíduo faleceu.
5. Agregações devem estar acompanhadas de cláusulas `GROUP BY` apropriadas.
6. Caso utilize `IDADE`, deve ser possível identificar o contexto (exemplo: média de idade ou distribuição por faixa etária).
7. Qualquer filtro ou cláusula `WHERE` deve ser consistente com os dados disponíveis no esquema.
   - Exemplo: Filtrar por `VAR8 = 'Alta'` está correto, mas `VAR8 = 'Média-Alta'` não existe.
8. Verifique se os nomes das colunas estão corretamente referenciados no contexto do esquema.
"""

def get_syntax_rules_message():
    """
    Retorna as regras para validação sintática.
    """
    return """
Regras de validação sintática:
- Verifique os seguintes problemas comuns:
  - Uso de `NOT IN` com valores NULL.
  - Uso de `UNION` quando `UNION ALL` deveria ser usado.
  - Uso de `BETWEEN` para intervalos exclusivos.
  - Mismatch de tipo de dados em predicados.
  - Identificadores não citados corretamente.
  - Número incorreto de argumentos para funções.
  - Cast para o tipo de dados incorreto.
  - Uso inadequado de colunas em joins.
"""

def get_response_format_message():
    """
    Retorna o formato esperado da resposta.
    """
    return """
Formato esperado da resposta:
- Se a query for válida, responda: "Válida: A query está correta."
- Se a query for inválida, responda: "Inválida: [Explique o problema encontrado]."
- Não forneça explicações adicionais ou corrija a query.
"""

def validate_query_syntax(query_sql):
    """
    Valida a sintaxe e aderência às regras de negócio de uma query SQL.
    """
    try:
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

