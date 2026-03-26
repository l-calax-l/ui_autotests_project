from urllib.parse import urljoin

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Конфигурация приложения для тестирования."""

    # --- Default settings ---
    default_time_out: float = 15
    poll_frequency: float = 1
    headless: bool = True
    use_grid: bool = False
    selenium_remote_url: str = Field(
        default="http://localhost:4444/wd/hub",
        description="URL хаба Selenium Grid"
    )

    # --- Way2automation ---
    base_url_1: str = Field(
        default="https://www.way2automation.com/",
        description="The base url for this application",
    )
    # --- Sql-ex ---
    base_url_2: str = Field(
        default="https://www.sql-ex.ru/",
        description="The base url for this application",
    )
    login: str = Field(description="Login")
    password: str = Field(description="Password")
    account_name: str = Field(description="Username")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    def get_full_url(self, base_url: str, path: str) -> str:
        return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


settings = Config()
