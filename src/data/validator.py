"""
Pulse Data Validation Utilities.

Provides clean, professional, and highly readable data checking routines
returning simple validation reports.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd
from src.config.logger import logger


@dataclass
class ValidationReport:
    """Simple summary of a dataset quality audit."""
    passed: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class PulseDataValidator:
    """
    Modular data validation tool designed to be simple, clean,
    and instantly understandable.
    """

    DEFAULT_MISSING_THRESHOLD: float = 0.20

    @classmethod
    def validate_not_empty(cls, df: pd.DataFrame) -> bool:
        """Verifies that the dataset contains records."""
        if df is None or df.empty:
            logger.error("Dataset check failed: Empty structure.")
            raise ValueError("Dataset validation failed: Dataframe contains zero rows.")
        
        logger.info("✓ Dataset not empty")
        return True

    @classmethod
    def validate_columns(cls, df: pd.DataFrame, required_columns: Optional[List[str]]) -> bool:
        """Verifies that all required column headers are present."""
        cls.validate_not_empty(df)
        
        if not required_columns:
            logger.info("✓ Required columns verified")
            return True
            
        missing_fields = [col for col in required_columns if col not in df.columns]
        if missing_fields:
            logger.error(f"Required columns missing: {missing_fields}")
            raise ValueError(f"Schema validation failed: Missing fields {missing_fields}")
            
        logger.info("✓ Required columns verified")
        return True

    @classmethod
    def validate_missing_values(
        cls, 
        df: pd.DataFrame, 
        threshold_percent: Optional[float] = None, 
        strict: bool = True
    ) -> ValidationReport:
        """Checks for missing data values against allowed limits."""
        cls.validate_not_empty(df)
        limit = threshold_percent if threshold_percent is not None else cls.DEFAULT_MISSING_THRESHOLD
        
        total_rows = len(df)
        null_counts = df.isnull().sum()
        
        breached_fields = {}
        warnings = []

        for column, null_count in null_counts.items():
            if null_count > 0:
                ratio = float(null_count / total_rows)
                if ratio > limit:
                    breached_fields[str(column)] = ratio
                    warnings.append(f"Column '{column}' is missing {ratio:.1%} of its data.")

        metrics = {"null_breached_fields": breached_fields}

        if breached_fields:
            if strict:
                logger.error("Missing value threshold exceeded.")
                raise ValueError(f"Data quality check failed: Fields exceeded threshold: {breached_fields}")
            else:
                logger.warning("Missing value threshold exceeded.")
                return ValidationReport(passed=False, warnings=warnings, metrics=metrics)

        logger.info("✓ Missing values within threshold")
        return ValidationReport(passed=True, metrics=metrics)

    @classmethod
    def validate_duplicates(
        cls, 
        df: pd.DataFrame, 
        subset_columns: Optional[List[str]] = None,
        strict: bool = True
    ) -> ValidationReport:
        """Checks for duplicate rows within the dataset."""
        cls.validate_not_empty(df)
        
        dup_count = int(df.duplicated(subset=subset_columns).sum())
        total_rows = len(df)
        dup_pct = float(dup_count / total_rows) if total_rows > 0 else 0.0
        
        metrics = {"duplicate_count": dup_count, "duplicate_percentage": dup_pct}
        errors = [f"Found {dup_count} duplicate rows ({dup_pct:.2%})."] if dup_count > 0 else []

        if dup_count > 0:
            if strict:
                logger.error("Duplicate rows detected.")
                raise ValueError(f"Data validation failed: Duplicate entries caught: {metrics}")
            else:
                logger.warning("Duplicate rows detected.")
                return ValidationReport(passed=False, errors=errors, metrics={"duplicate_statistics": metrics})

        logger.info("✓ Duplicate check passed")
        return ValidationReport(passed=True, metrics={"duplicate_statistics": metrics})

    @classmethod
    def validate_datatypes(cls, df: pd.DataFrame, expected_types: Dict[str, str]) -> bool:
        """Verifies columns match logical types (numeric, string, datetime)."""
        cls.validate_not_empty(df)
        
        for column, type_rule in expected_types.items():
            if column in df.columns:
                series = df[column]
                tag = type_rule.lower().strip()
                is_valid = False
                
                if tag == "numeric":
                    is_valid = bool(pd.api.types.is_numeric_dtype(series))
                elif tag == "string":
                    is_valid = bool(pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series))
                elif tag == "datetime":
                    is_valid = bool(pd.api.types.is_datetime64_any_dtype(series))
                else:
                    raise ValueError(f"Invalid validation datatype target rule: '{type_rule}'")
                    
                if not is_valid:
                    logger.error(f"Invalid datatype for column: '{column}'.")
                    raise TypeError(f"Type safety violation: Field '{column}' must match type '{tag}'")
                    
        logger.info("✓ Datatypes verified")
        return True

    @classmethod
    def validate(
        cls, 
        df: pd.DataFrame, 
        required_columns: Optional[List[str]] = None, 
        expected_types: Optional[Dict[str, str]] = None,
        max_missing_ratio: Optional[float] = None,
        unique_subset: Optional[List[str]] = None,
        strict: bool = True
    ) -> ValidationReport:
        """Runs the complete data validation pipeline sequentially."""
        logger.info("Starting dataset validation...")
        
        # Core checks that will raise exceptions directly if they fail
        cls.validate_not_empty(df)
        cls.validate_columns(df, required_columns)
        
        # Pipeline checks that can run in strict or warning mode
        missing_report = cls.validate_missing_values(df, threshold_percent=max_missing_ratio, strict=strict)
        duplicate_report = cls.validate_duplicates(df, subset_columns=unique_subset, strict=strict)
        
        if expected_types:
            cls.validate_datatypes(df, expected_types)
            
        # Combine metrics and status flags cleanly
        is_passed = bool(missing_report.passed and duplicate_report.passed)
        combined_metrics = {**missing_report.metrics, **duplicate_report.metrics}
        
        logger.info("Dataset validation completed successfully.")
        return ValidationReport(
            passed=is_passed,
            warnings=missing_report.warnings,
            errors=duplicate_report.errors,
            metrics=combined_metrics
        )
