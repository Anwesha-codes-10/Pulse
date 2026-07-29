from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "Pulse"

    VERSION: str = "1.0.0"

    RANDOM_SEED: int = 42

    FORECAST_WINDOWS = (7, 30, 90)

    LOG_LEVEL: str = "INFO"


settings = Settings()