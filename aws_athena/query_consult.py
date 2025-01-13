import boto3
import pandas as pd
import time
import os
import awswrangler as wr


region_name = "us-east-1"
database = "chatbot_athena_db"
output_location = "s3://chatbot-dados-analise/result/"

athena_client = boto3.client("athena", region_name=region_name)


def execute_query(query, database, output_location):
    """
    Executa uma consulta no Athena e retorna o resultado como um Pandas DataFrame.
    """
    print(os.environ)
    try:
        # Executar a consulta
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
        )
        query_execution_id = response["QueryExecutionId"]
        print(f"Consulta iniciada. ID: {query_execution_id}")

        # Aguardar a execução da consulta
        status = "RUNNING"
        while status in ["RUNNING", "QUEUED"]:
            response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response["QueryExecution"]["Status"]["State"]
            if status == "SUCCEEDED":
                print("Consulta concluída com sucesso.")
            elif status in ["FAILED", "CANCELLED"]:
                raise Exception(f"Consulta falhou: {response['QueryExecution']['Status']['StateChangeReason']}")
            time.sleep(1)

        # Obter o resultado da consulta
        result_file_path = f"{output_location}{query_execution_id}.csv"
        print(f"Resultado salvo em: {result_file_path}")

        # Ler o arquivo CSV do S3 e converter para DataFrame
        s3_client = boto3.client("s3")
        bucket_name = output_location.split("/")[2]
        key = "/".join(output_location.split("/")[3:] + [f"{query_execution_id}.csv"])
        
        # Baixar o arquivo do S3
        # s3_client.download_file(bucket_name, key, "query_result.csv")
        df = wr.s3.read_csv(result_file_path, encoding='ISO-8859-1', path_suffix="csv")
        return df

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None



