from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str
    pinecone_api_key: str
    pinecone_index_name: str = "rag-knowledge-assistant"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()