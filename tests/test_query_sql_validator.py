import pytest
from unittest.mock import MagicMock
from models.query_sql_validator import contains_prohibited_keywords, construct_validation_message, validate_query_syntax

def test_contains_prohibited_keywords():
    """Teste para detectar palavras-chave proibidas na query."""
    assert contains_prohibited_keywords("SELECT * FROM tabela;") is False
    assert contains_prohibited_keywords("INSERT INTO tabela VALUES ('1', '2');") is True
    assert contains_prohibited_keywords("UPDATE tabela SET coluna = 'valor';") is True
    assert contains_prohibited_keywords("ALTER TABLE tabela ADD coluna INT;") is True
    assert contains_prohibited_keywords("TRUNCATE TABLE tabela;") is True

def test_construct_validation_message():
    """Teste para verificar se o prompt de validação é construído corretamente."""
    message = construct_validation_message()
    assert "Você é um assistente especializado em validação de queries SQL" in message
    assert "Regras de validação" in message
    assert "Formato esperado" in message

@pytest.fixture
def mock_chat(mocker):
    """Mock para o ChatOpenAI."""
    mock_chat = mocker.patch("models.query_sql_validator.chat")
    mock_chat.invoke = MagicMock()
    return mock_chat

def test_validate_query_syntax_valid(mock_chat):
    """Teste para validar uma query SQL válida."""
    mock_chat.invoke.return_value.content = "Válida: A query está correta."
    response = validate_query_syntax("SELECT * FROM tabela;")
    assert response["valido"] is True
    assert response["racional"] == "Válida: A query está correta."

def test_validate_query_syntax_invalid_keyword(mock_chat):
    """Teste para verificar queries contendo palavras-chave proibidas."""
    response = validate_query_syntax("INSERT INTO tabela VALUES ('1', '2');")
    assert response["valido"] is False
    assert "A query contém operações proibidas" in response["racional"]

def test_validate_query_syntax_invalid_syntax(mock_chat):
    """Teste para verificar o comportamento em caso de erro de sintaxe na query."""
    mock_chat.invoke.return_value.content = "Inválida: Sintaxe incorreta."
    response = validate_query_syntax("SELECT FROM tabela;")
    assert response["valido"] is False
    assert response["racional"] == "Inválida: Sintaxe incorreta."
