from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    use_local_explainer: bool = False
    local_explainer_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    max_input_chars: int = 12000
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


settings = Settings()
