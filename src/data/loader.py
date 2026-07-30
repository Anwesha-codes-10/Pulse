"""
Pulse Data Loader Utilities.

Provides centralized, reusable mechanisms for loading and saving dataset matrices
securely across stratified application workspace storage directories.
"""

from pathlib import Path
import pandas as pd
from src.config.logger import logger
from src.config.paths import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
)


class PulseDataLoader:
    """Production-grade data ingestion manager handling isolated CSV file transitions."""

    CATEGORY_PATHS: dict[str, Path] = {
        "raw": RAW_DATA_DIR,
        "processed": PROCESSED_DATA_DIR,
        "external": EXTERNAL_DATA_DIR,
    }

    @classmethod
    def _resolve_directory(cls, category: str) -> Path:
        """
        Return the directory corresponding to the given storage category.

        Args:
            category: Target partition folder (raw, processed, or external).

        Returns:
            Path object pointing to the requested directory structure.

        Raises:
            ValueError: If an unrecognized storage layer name is provided.
        """
        directory = cls.CATEGORY_PATHS.get(category.lower())

        if directory is None:
            raise ValueError(
                f"Invalid category '{category}'. "
                f"Choose from: {list(cls.CATEGORY_PATHS.keys())}"
            )

        return directory

    @classmethod
    def _validate_filename(cls, filename: str) -> str:
        """
        Validates, sanitizes, and hard-fences input string parameters for safe storage I/O.

        Args:
            filename: Target input string parameter to verify.

        Returns:
            A sanitized, traversal-safe base filename string.

        Raises:
            ValueError: If parameters are blank, missing, or do not end with a .csv token.
        """
        clean_filename = filename.strip() if filename else ""
        
        # Enforce case-insensitive verification checks safely
        if not clean_filename or not clean_filename.lower().endswith(".csv"):
            raise ValueError("Filename parameter must be a non-empty string ending with '.csv'")
            
        # Defend strictly against path-traversal vulnerabilities (e.g. '../../malicious.csv')
        # by extracting only the pure file name component via strict Path parsing
        sanitized_name = Path(clean_filename).name
        
        return sanitized_name

    @classmethod
    def load_csv(
        cls,
        filename: str,
        category: str = "raw",
    ) -> pd.DataFrame:
        """
        Load a target CSV file into an active Pandas DataFrame with tracing.

        Args:
            filename: Name of the target CSV file on disk.
            category: Storage tier partition location ('raw', 'processed', 'external').

        Returns:
            A populated Pandas DataFrame.

        Raises:
            ValueError: If file parameters or formats are structurally invalid.
            FileNotFoundError: If the target file is missing from the disk layout.
            RuntimeError: If data parsing fails unexpectedly.
        """
        sanitized_filename = cls._validate_filename(filename)
        directory = cls._resolve_directory(category)
        file_path = directory / sanitized_filename

        logger.info(f"Loading CSV from disk layer: {file_path}")

        if not file_path.exists():
            logger.error(f"Target data file asset missing on disk: {file_path}")
            raise FileNotFoundError(f"Required dataset asset not found at path: '{file_path}'")

        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded dataset successfully | Shape: {df.shape}")
            return df

        except Exception as err:
            logger.exception("Failed to load CSV due to underlying data stream corruption.")
            raise RuntimeError(f"Failed to load dataset file '{sanitized_filename}'") from err

    @classmethod
    def save_csv(
        cls,
        df: pd.DataFrame,
        filename: str,
        category: str = "processed",
        index: bool = False,
    ) -> Path:
        """
        Save an active operational DataFrame safely out to local disk architecture.

        Args:
            df: Source Pandas DataFrame payload to serialize.
            filename: Target output file name to write.
            category: Destination partition tier ('raw', 'processed').
            index: Flag determining if row tracking indices are saved.

        Returns:
            The resolved absolute Path object where the file was successfully stored.

        Raises:
            ValueError: If file names are malformed or missing parameters.
            RuntimeError: If disk persistence fails during compilation.
        """
        sanitized_filename = cls._validate_filename(filename)
        directory = cls._resolve_directory(category)
        
        # Proactively verify that the destination directory hierarchy exists before saving
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / sanitized_filename

        if df.empty:
            logger.warning(f"Detected empty DataFrame payload arriving for serialization at path: {file_path}")

        logger.info(f"Saving CSV data matrix to disk node: {file_path}")

        try:
            df.to_csv(file_path, index=index)
            logger.info("Dataset saved successfully.")
            return file_path

        except Exception as err:
            logger.exception("Failed to save CSV out to disk architecture layer.")
            raise RuntimeError(f"Failed to save dataset file '{sanitized_filename}'") from err
