
import json
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "sample_companies.csv"
CLEANED_FILE = BASE_DIR / "cleaned_companies.csv"
REJECTED_FILE = BASE_DIR / "rejected_companies.csv"
REPORT_FILE = BASE_DIR / "report.json"

EMAIL_PATTERN = (
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def clean_data():
    df = pd.read_csv(INPUT_FILE)
    total_input = len(df)

    # Clean text fields and standardize blank cells.
    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:
        df[column] = df[column].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df["email"] = df["email"].str.lower()

    # Validate required fields and email format.
    has_company = df["company_name"].notna()
    has_email = df["email"].notna()
    valid_email = df["email"].str.match(
        EMAIL_PATTERN, na=False
    )

    valid_mask = has_company & has_email & valid_email

    rejected = df.loc[~valid_mask].copy()

    def rejection_reason(row):
        reasons = []

        if pd.isna(row["company_name"]):
            reasons.append("Missing company name")

        if pd.isna(row["email"]):
            reasons.append("Missing email")
        elif not re.fullmatch(
            EMAIL_PATTERN, str(row["email"])
        ):
            reasons.append("Invalid email format")

        return "; ".join(reasons)

    rejected["rejection_reason"] = rejected.apply(
        rejection_reason, axis=1
    )

    # Remove duplicate email addresses from valid records.
    valid_rows = df.loc[valid_mask].copy()
    duplicate_count = int(
        valid_rows.duplicated(subset=["email"]).sum()
    )

    cleaned = valid_rows.drop_duplicates(
        subset=["email"], keep="first"
    )

    # Save all outputs.
    cleaned.to_csv(CLEANED_FILE, index=False)
    rejected.to_csv(REJECTED_FILE, index=False)

    report = {
        "total_input_rows": int(total_input),
        "cleaned_rows": int(len(cleaned)),
        "rejected_rows": int(len(rejected)),
        "duplicate_records_removed": duplicate_count,
        "missing_values_by_column": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
        "output_files": [
            CLEANED_FILE.name,
            REJECTED_FILE.name,
        ],
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("DATA CLEANING COMPLETED")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    clean_data()
