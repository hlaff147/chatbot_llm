import re

def extract_sql_query(response_content):
    """Extrai a query SQL de uma resposta com delimitadores ```sql."""
    match = re.search(r"```sql\n(.*?)```", response_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("Nenhuma query SQL encontrada na resposta do GPT.")
