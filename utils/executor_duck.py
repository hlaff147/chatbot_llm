import duckdb

def execute_query_on_dataframe(query, df):
    """Executa uma query SQL em um DataFrame usando DuckDB."""
    try:
        result = duckdb.query(query).df()
        return result
    except Exception as e:
        return f"Erro ao executar a query: {e}"
