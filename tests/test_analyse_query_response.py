import pytest
from unittest.mock import MagicMock
from models.analyse_query_response import construct_analysis_message, analyse_response_query

@pytest.fixture
def mock_chat(mocker):
    """Mock para o ChatOpenAI."""
    mock_chat = mocker.patch("models.analyse_query_response.chat")
    mock_chat.invoke = MagicMock()
    return mock_chat

def test_construct_analysis_message():
    """Teste para garantir que a mensagem de análise é construída corretamente."""
    message = construct_analysis_message()
    assert "Você é um assistente especializado em análise de dados SQL." in message
    assert "- REF_DATE: Data de referência do registro." in message
    assert "Forneça um parágrafo explicativo." in message

def test_analyse_response_query_valid(mock_chat):
    """Teste para a análise de uma query com resultado válido."""
    mock_chat.invoke.return_value.content = "O estado com maior inadimplência é SP, com 40%."
    query_result = [
        {"UF": "SP", "Inadimplencia": 0.4},
        {"UF": "RJ", "Inadimplencia": 0.3},
    ]
    response = analyse_response_query(query_result)
    mock_chat.invoke.assert_called_once()
    assert response["resultado_query"] == query_result
    assert response["analise"] == "O estado com maior inadimplência é SP, com 40%."

def test_analyse_response_query_empty_result(mock_chat):
    """Teste para análise de uma query com resultado vazio."""
    mock_chat.invoke.return_value.content = "Nenhum dado disponível para análise."
    query_result = []
    response = analyse_response_query(query_result)
    mock_chat.invoke.assert_called_once()
    assert response["resultado_query"] == query_result
    assert response["analise"] == "Nenhum dado disponível para análise."

def test_analyse_response_query_error(mock_chat):
    """Teste para análise com erro durante a execução."""
    mock_chat.invoke.side_effect = Exception("Falha na comunicação com o modelo.")
    query_result = [
        {"UF": "SP", "Inadimplencia": 0.4},
        {"UF": "RJ", "Inadimplencia": 0.3},
    ]
    response = analyse_response_query(query_result)
    mock_chat.invoke.assert_called_once()
    assert response["resultado_query"] == query_result
    assert "erro" in response
    assert "Falha na comunicação com o modelo." in response["erro"]
