import streamlit as st
import pandas as pd
import json
from aws_athena.query_consult import execute_query
from config.settings import csv_path
from models.analyse_query_response import analyse_response_query
from models.input_validator import validate_user_input
from models.query_generator import generate_query
from models.query_sql_validator import validate_query_syntax
from utils.sql_extractor import extract_sql_query

df = pd.read_csv(csv_path)

st.title("Chatbot de Análise de Dados SQL")
st.subheader("Interaja com seu dataset de forma intuitiva!")

user_input = st.text_input("Digite sua pergunta:", placeholder="Exemplo: Qual a média de idade por UF?")

if st.button("Executar"):
    st.write("**Validando entrada...**")
    validation_result = validate_user_input(user_input)
    validation_result_dict = json.loads(validation_result)

    if not validation_result_dict["valido"]:
        st.error(f"Entrada inválida: {validation_result_dict['racional']}")
    else:
        st.write("**Gerando query SQL...**")
        sql_response = generate_query(user_input)
        sql_query = extract_sql_query(sql_response)

        
        sql_query_replaced = sql_query.replace("tabela", "credit")
        st.code(f"Query SQL Gerada:\n{sql_query_replaced}", language="sql")

        validation_result = validate_query_syntax(sql_query_replaced)

        if not validation_result["valido"]:
            st.error(f"Query Inválida: {validation_result['racional']}")
            st.stop()

        st.success("Query SQL validada com sucesso!")

        st.write("**Executando query no dataset...**")
        
        df_result = execute_query(sql_query_replaced, "chatbot_athena_db", "s3://chatbot-dados-analise/result/")

        if df_result is not None:
          print("Resultado da Consulta:")
          print(df_result)
        else:
          print("A consulta falhou.")

        if isinstance(df_result, pd.DataFrame):
            st.write("**Resultado da Query:**")
            st.dataframe(df_result)

            st.write("**Gerando análise explicativa...**")
            analysis = analyse_response_query(df_result)
            st.write("**Resposta reformulada:**")
            st.write(analysis["analise"])
        else:
            st.error(f"Erro ao executar a query: {df_result}")
