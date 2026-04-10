from pydantic_settings import BaseSettings, SettingsConfigDict
import json

class Settings(BaseSettings):
    SQL_SERVER: str
    SQL_DB: str
    SQL_USER: str
    SQL_PASSWORD: str

    DEVICE_PRINT_POLICY_SERIAL: dict = {}
    DEVICE_PRINT_POLICY_NAME: dict = {}

    COOLDOWN_MINUTES: int = 5
    POLL_INTERVAL: float = 0.5
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/mealslip.log"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def __init__(self, **data):
        super().__init__(**data)
        # Parse JSON strings from .env
        if isinstance(self.DEVICE_PRINT_POLICY_SERIAL, str):
            self.DEVICE_PRINT_POLICY_SERIAL = json.loads(self.DEVICE_PRINT_POLICY_SERIAL)
        if isinstance(self.DEVICE_PRINT_POLICY_NAME, str):
            self.DEVICE_PRINT_POLICY_NAME = json.loads(self.DEVICE_PRINT_POLICY_NAME)

settings = Settings()