from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict
import urllib.parse

class Settings(BaseSettings):
    # App config
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")

    # LLM config
    llm_url: str = Field(..., env="LLM_URL")
    llm_key: str = Field(..., env="LLM_KEY")
    llm_model: str = Field(..., env="LLM_MODEL")
    openai_llm_url: str = Field(..., env="OPENAI_LLM_URL")
    max_tokens : int = Field(...,env="MAX_TOKENS")
    max_turns : int = Field(...,env="MAX_TURNS")


    # Database config
    db_server: str = Field(..., env="DB_SERVER")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_driver: str = Field("ODBC Driver 18 for SQL Server", env="DB_DRIVER")
    allowed_origins: list[str] = Field(default=["*"], env="ALLOWED_ORIGINS")

    #postgres connection
    postgresql_server: str = Field(..., env="POSTGRESQL_SERVER")
    postgresql_name: str = Field(..., env="POSTGRESQL_NAME")
    postgresql_user: str = Field(..., env="POSTGRESQL_USER")
    postgresql_pass: str = Field(..., env="POSTGRESQL_PASS")
    postgresql_port : str = Field(...,env="POSTGRESQL_PORT")
    excel_uploaded_dir : str = Field(...,env="EXCEL_UPLOADED_DIR")

    @property
    def sqlserver_db_connection_string(self) -> str:
        return (
            f"mssql+pyodbc://{self.db_user}:{self.db_pass}"
            f"@{self.db_server}/{self.db_name}?driver={self.db_driver}"
        )
        # return (
        #     f"mssql+pyodbc://@{self.db_server}/{self.db_name}"
        #     f"?driver={self.db_driver}&trusted_connection=yes&TrustServerCertificate=yes"
        # )
    @property
    def postgresql_connection_string(self) -> str:
        password_encoded = urllib.parse.quote_plus(self.postgresql_pass)
        return (
        f"postgresql://{self.postgresql_user}:{password_encoded}"
        f"@{self.postgresql_server}:{self.postgresql_port}/{self.postgresql_name}"
    )
    @property
    def postgresql_sqlalchemy_connection_string(self) -> str:
        password_encoded = urllib.parse.quote_plus(self.postgresql_pass)
        return (
        f"postgresql+psycopg2://{self.postgresql_user}:{password_encoded}"
        f"@{self.postgresql_server}:{self.postgresql_port}/{self.postgresql_name}"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Singleton instance
settings = Settings()


