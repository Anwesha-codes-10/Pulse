from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = SRC_DIR / "models"

LOGS_DIR = PROJECT_ROOT / "logs"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"

TESTS_DIR = PROJECT_ROOT / "tests"