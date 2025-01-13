import streamlit as st
import pandas as pd
import json
from config.settings import csv_path
from models.analyse_query_response import analyse_response_query
from models.input_validator import validate_user_input
from models.query_generator import generate_query
from models.query_sql_validator import validate_query_syntax
from utils.sql_extractor import extract_sql_query
from utils.executor_duck import execute_query_on_dataframe

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

        
        sql_query_replaced = sql_query.replace("tabela", "df")
        st.code(f"Query SQL Gerada:\n{sql_query_replaced}", language="sql")
        
        # Validar a query SQL
        # st.write("**Validando a query SQL...**")
        # validation_result = validate_query_syntax(sql_query_replaced)
        
        # Verificar se a query é válida
        # if validation_result["valido"]:
        #     st.success("A query SQL é válida!")
        #     st.write("Racional:")
        #     st.write(validation_result["racional"])
        # else:
        #     st.error("A query SQL é inválida!")
        #     st.write("Erro encontrado:")
        #     st.write(validation_result["racional"])
        #     st.stop()  # Interrompe a execução do Streamlit

        st.write("**Executando query no dataset...**")
        result = execute_query_on_dataframe(sql_query_replaced, df)

        if isinstance(result, pd.DataFrame):
            st.write("**Resultado da Query:**")
            st.dataframe(result)

            st.write("**Gerando análise explicativa...**")
            analysis = analyse_response_query(result)
            st.write("**Resposta reformulada:**")
            st.write(analysis["analise"])
        else:
            st.error(f"Erro ao executar a query: {result}")
