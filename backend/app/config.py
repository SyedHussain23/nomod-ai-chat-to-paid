from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    claude_model: str = "claude-opus-4-7"
    app_env: str = "development"
    base_payment_url: str = "https://pay.nomod.ai/pay"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"


settings = Settings()
