from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    firebase_client_email: str = ""
    firebase_private_key: str = ""
    firebase_project_id: str = ""
    posts_collection: str = "AiPosts"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
