import pytest
from utils.sql_extractor import extract_sql_query

def test_extract_sql_query_valid():
    """Teste para uma resposta válida contendo uma query SQL."""
    response_content = """Aqui está sua query:
    ```sql
    SELECT * FROM tabela;
    ```
    Espero que isso resolva sua dúvida."""
    result = extract_sql_query(response_content)
    assert result == "SELECT * FROM tabela;"

def test_extract_sql_query_no_query():
    """Teste para uma resposta sem uma query SQL."""
    response_content = """Desculpe, não consegui encontrar uma query para sua solicitação."""
    with pytest.raises(ValueError, match="Nenhuma query SQL encontrada na resposta do GPT."):
        extract_sql_query(response_content)

def test_extract_sql_query_no_delimiters():
    """Teste para uma resposta sem delimitadores de bloco SQL."""
    response_content = """Aqui está sua query:
    SELECT * FROM tabela;
    Espero que isso ajude."""
    with pytest.raises(ValueError, match="Nenhuma query SQL encontrada na resposta do GPT."):
        extract_sql_query(response_content)
