import pytest
from unittest.mock import MagicMock
from models.query_generator import (
    dataset_description,
    query_rules,
    output_format,
    construct_system_message,
    generate_query
)

@pytest.fixture
def mock_chat(mocker):
    """Mock para o ChatOpenAI."""
    mock_chat = mocker.patch("models.query_generator.chat")
    mock_chat.invoke = MagicMock()
    return mock_chat

def test_dataset_description():
    """Teste: Verifica se a descrição do dataset contém as colunas necessárias."""
    description = dataset_description()
    assert "REF_DATE (Coluna)" in description
    assert "VAR8 (Coluna)" in description
    assert "Não substitua ou modifique os nomes das colunas" in description

def test_query_rules():
    """Teste: Verifica se as regras de query estão corretamente definidas."""
    rules = query_rules()
    assert "Utilize exclusivamente as colunas identificadas como (Coluna) acima." in rules
    assert "Certifique-se de que o nome da tabela é \"tabela\"." in rules
    assert "Sempre agrupe os resultados (`GROUP BY`) quando necessário" in rules

def test_output_format():
    """Teste: Verifica se o formato esperado da saída está correto."""
    format_info = output_format()
    assert "Retorne apenas a query SQL, delimitada pelo bloco ```sql." in format_info
    assert "Não inclua explicações adicionais ou comentários no retorno." in format_info

def test_construct_system_message():
    """Teste: Verifica se a mensagem do sistema é construída corretamente."""
    message = construct_system_message()
    assert "Você é um assistente especializado em análise de dados SQL." in message
    assert "Agora, transforme a seguinte pergunta em uma query SQL:" in message
    assert "REF_DATE (Coluna)" in message  # Certifica-se de que as colunas estão listadas

def test_generate_query_valid(mock_chat):
    """Teste: Garante que uma query SQL válida seja gerada."""
    # Mock da resposta do ChatOpenAI
    mock_chat.invoke.return_value.content = """```sql
    SELECT VAR5, AVG(IDADE) FROM tabela GROUP BY VAR5;
    ```"""
    user_input = "Qual a média de idade por estado?"
    query = generate_query(user_input)
    assert "SELECT VAR5, AVG(IDADE)" in query
    assert "GROUP BY VAR5" in query

def test_generate_query_invalid(mock_chat):
    """Teste: Verifica o comportamento quando uma pergunta inválida é fornecida."""
    # Mock da resposta do ChatOpenAI
    mock_chat.invoke.return_value.content = "Inválida: Não foi possível gerar uma query válida."
    user_input = "Calcule algo impossível no dataset."
    query = generate_query(user_input)
    assert "Inválida" in query
    assert "Não foi possível gerar uma query válida." in query
