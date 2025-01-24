from enum import Enum

class Role(Enum):
    VALIDATION_QUESTION = "validation_question"
    GENERATE_QUERY = "generate_query"
    VALIDATE_QUERY = "validate_query"
    GENERATE_INSIGHTS = "generate_insights"
