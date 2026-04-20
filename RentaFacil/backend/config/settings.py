from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "rentafacil"
    environment: str = "docker"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    stripe_secret_key: str = ""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    frontend_url: str = "http://localhost:3002"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
