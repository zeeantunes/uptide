from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configurações da aplicação.
    Carrega variáveis do arquivo .env automaticamente.
    """

    #Stripe
    stripe_api_key: str
    stripe_webhook_secret: str

    #Supabase
    supabase_url: str
    supabase_key: str

    #App
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensetive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações (cached).
    O cache evita ler o .env múltiplas vezes.
    """
    return Settings()