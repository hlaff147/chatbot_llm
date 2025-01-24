from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY
from enums.role_enum import Role

class ChatFactory:
    @staticmethod
    def create_chat(role: Role):
        """
        Cria uma instância do ChatOpenAI com base no contexto (role).
        """
        configs = {
            Role.VALIDATION_QUESTION: {
                "model": "gpt-4",
                "temperature": 0,
                "model_kwargs": {"response_format": {"type": "json_object"}},
            },
            Role.GENERATE_QUERY: {
                "model": "gpt-3.5-turbo",
                "temperature": 0.2,
                "model_kwargs": {"response_format": {"type": "text"}},
            },
            Role.VALIDATE_QUERY: {
                "model": "gpt-3.5-turbo",
                "temperature": 0,
                "model_kwargs": {"response_format": {"type": "json_object"}},
            },
            Role.GENERATE_INSIGHTS: {
                "model": "gpt-4",
                "temperature": 0.7,
                "model_kwargs": {"response_format": {"type": "text"}},
            },
        }

        if role not in configs:
            raise ValueError(f"Role desconhecido: {role}")

        config = configs[role]
        return ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            openai_api_key=OPENAI_API_KEY,
            model_kwargs=config["model_kwargs"]
        )
