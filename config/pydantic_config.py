from urllib.parse import urljoin

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    base_url: str = Field(
        default="https://www.way2automation.com/",
        description="The base url for this application",
    )
    default_time_out: float = 15
    poll_frequency: float = 1
    headless: bool = True
    selenium_remote_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    def get_full_url(self, path: str) -> str:
        return urljoin(self.base_url.rstrip("/") + "/", path.lstrip("/"))


settings = Config()
