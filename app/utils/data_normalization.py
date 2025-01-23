import pandas as pd
import re

def normalize_column(df, column_name, dtype="float"):
    """Normalize a column by ensuring numeric conversion and handling missing values."""
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' is missing in the dataset.")
    return pd.to_numeric(df[column_name], errors="coerce").fillna(0).astype(dtype)

def normalize_term(value):
    """Normalize term values to months."""
    if pd.isnull(value):
        return None
    value = value.strip().lower()
    match = re.search(r"(\d+)", value)
    if not match:
        return None
    numeric_value = int(match.group(1))
    return numeric_value * 12 if "year" in value else numeric_value

def normalize_emp_length(value):
    """Convert employment length to numeric values."""
    if pd.isnull(value):
        return 0
    if "10+" in value:
        return 10
    if "< 1" in value:
        return 0.5
    match = re.search(r"(\d+)", value)
    return float(match.group(1)) if match else 0
