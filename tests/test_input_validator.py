import pytest
from unittest.mock import MagicMock
from models.input_validator import construct_validation_message, validate_user_input

@pytest.fixture
def mock_chat(mocker):
    """Mock para o ChatOpenAI."""
    mock_chat = mocker.patch("models.input_validator.chat")
    mock_chat.invoke = MagicMock()
    return mock_chat

def test_construct_validation_message():
    """Teste para garantir que a mensagem de validação é construída corretamente."""
    message = construct_validation_message()
    assert "Você é um assistente especializado em validação de entradas" in message
    assert "REF_DATE: Data de referência do registro." in message
    assert "A pergunta deve usar apenas as colunas disponíveis listadas acima." in message
    assert "Formato da resposta (JSON)" in message

def test_validate_user_input_valid(mock_chat):
    """Teste para input válido."""
    # Mock da resposta do ChatOpenAI
    mock_chat.invoke.return_value.content = """
    {
        "racional": "A pergunta é válida e usa apenas colunas do esquema do banco.",
        "valido": true
    }
    """
    user_input = "Qual a média de idade por estado?"
    response = validate_user_input(user_input)
    assert '"valido": true' in response
    assert '"racional": "A pergunta é válida e usa apenas colunas do esquema do banco."' in response

def test_validate_user_input_invalid_column(mock_chat):
    """Teste para input que usa uma coluna inexistente."""
    # Mock da resposta do ChatOpenAI
    mock_chat.invoke.return_value.content = """
    {
        "racional": "A pergunta faz referência a uma coluna inexistente no esquema do banco.",
        "valido": false
    }
    """
    user_input = "Qual é o total de vendas por estado?"
    response = validate_user_input(user_input)
    assert '"valido": false' in response
    assert '"racional": "A pergunta faz referência a uma coluna inexistente no esquema do banco."' in response

def test_validate_user_input_unclear_question(mock_chat):
    """Teste para input que não é claro."""
    # Mock da resposta do ChatOpenAI
    mock_chat.invoke.return_value.content = """
    {
        "racional": "A pergunta não é clara o suficiente para gerar uma query SQL válida.",
        "valido": false
    }
    """
    user_input = "Quero saber os dados, por favor."
    response = validate_user_input(user_input)
    assert '"valido": false' in response
    assert '"racional": "A pergunta não é clara o suficiente para gerar uma query SQL válida."' in response
