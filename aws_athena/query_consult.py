import os
import time
import boto3
import awswrangler as wr

class AthenaQueryExecutor:
    def __init__(self, athena_client=None, sleep_interval=1):
        """
        Inicializa o executor de consultas do Athena.
        
        :param athena_client: Instância personalizada do cliente do Athena (opcional).
        :param sleep_interval: Intervalo de tempo (em segundos) entre verificações de status.
        """
        self.athena_client = athena_client or boto3.client("athena")
        self.sleep_interval = sleep_interval

    def execute_query(self, query, database, output_location):
        """
        Executa uma consulta no Athena e retorna o resultado como um Pandas DataFrame.
        
        :param query: A consulta SQL a ser executada.
        :param database: O banco de dados no Athena.
        :param output_location: O local de saída no S3 para armazenar os resultados.
        :return: Pandas DataFrame contendo os resultados da consulta.
        """
        try:
            query_execution_id = self._start_query_execution(query, database, output_location)
            self._wait_for_query_to_complete(query_execution_id)
            return self._fetch_query_results(output_location, query_execution_id)
        except Exception as e:
            self._log_error(f"Erro ao executar a consulta: {e}")
            return None

    def _start_query_execution(self, query, database, output_location):
        """
        Inicia a execução da consulta no Athena.
        
        :return: ID de execução da consulta.
        """
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
        )
        query_execution_id = response["QueryExecutionId"]
        self._log_info(f"Consulta iniciada. ID: {query_execution_id}")
        return query_execution_id

    def _wait_for_query_to_complete(self, query_execution_id):
        """
        Aguarda a conclusão da consulta no Athena.
        
        :param query_execution_id: ID de execução da consulta.
        """
        status = "RUNNING"
        while status in ["RUNNING", "QUEUED"]:
            response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response["QueryExecution"]["Status"]["State"]
            if status == "SUCCEEDED":
                self._log_info("Consulta concluída com sucesso.")
            elif status in ["FAILED", "CANCELLED"]:
                raise Exception(f"Consulta falhou: {response['QueryExecution']['Status']['StateChangeReason']}")
            time.sleep(self.sleep_interval)

    def _fetch_query_results(self, output_location, query_execution_id):
        """
        Obtém os resultados da consulta do S3 e retorna como um DataFrame.
        
        :param output_location: Caminho do S3 onde os resultados foram salvos.
        :param query_execution_id: ID de execução da consulta.
        :return: Pandas DataFrame contendo os resultados.
        """
        result_file_path = f"{output_location}{query_execution_id}.csv"
        self._log_info(f"Resultado salvo em: {result_file_path}")
        return wr.s3.read_csv(result_file_path, encoding="ISO-8859-1", path_suffix="csv")

    @staticmethod
    def _log_info(message):
        """
        Registra uma mensagem de informação.
        
        :param message: Mensagem a ser registrada.
        """
        print(f"[INFO] {message}")

    @staticmethod
    def _log_error(message):
        """
        Registra uma mensagem de erro.
        
        :param message: Mensagem a ser registrada.
        """
        print(f"[ERROR] {message}")
