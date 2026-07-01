# modules/cleaner.py

import pandas as pd


def clean_data(df):
    """
    Accepts a raw DataFrame from the loader.
    Returns a tuple: (cleaned DataFrame, cleaning report dict)
    """
    report = {
        "original_rows": len(df),
        "duplicates_removed": 0,
        "missing_values_filled": 0,
        "invalid_marks_found": 0,
        "columns_renamed": [],
        "marks_columns": []
    }

    # ── Step 1: Clean column names ────────────────────────────────────────────
    original_columns = list(df.columns)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    renamed = [
        f"{old} → {new}"
        for old, new in zip(original_columns, df.columns)
        if old != new
    ]
    report["columns_renamed"] = renamed

    # ── Step 2: Drop fully duplicate rows ────────────────────────────────────
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    # ── Step 3: Identify marks columns ───────────────────────────────────────
    # Assume any column that isn't student_id or name is a marks column
    non_marks = ["student_id", "name", "roll_no", "roll", "id"]
    marks_cols = [col for col in df.columns if col not in non_marks]
    report["marks_columns"] = marks_cols

    # ── Step 4: Coerce marks columns to numeric ───────────────────────────────
    for col in marks_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ── Step 5: Record and fill missing values ────────────────────────────────
    missing_before = df[marks_cols].isna().sum().sum()
    report["missing_values_filled"] = int(missing_before)
    df[marks_cols] = df[marks_cols].fillna(0)

    # ── Step 6: Validate mark ranges (0–100) ─────────────────────────────────
    invalid_mask = (df[marks_cols] < 0) | (df[marks_cols] > 100)
    report["invalid_marks_found"] = int(invalid_mask.sum().sum())
    # Clip invalid values to valid range rather than dropping
    df[marks_cols] = df[marks_cols].clip(lower=0, upper=100)

    # ── Step 7: Final row count ───────────────────────────────────────────────
    report["final_rows"] = len(df)

    return df, report