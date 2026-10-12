
# Automated Company Data Cleaning Pipeline

## Overview
A Python-based data cleaning pipeline that processes company
records from a CSV file, validates required fields, removes
duplicate email addresses, and generates a JSON summary report.

## Features
- CSV data ingestion using Pandas
- Text normalization and email standardization
- Missing-value detection
- Email format validation
- Duplicate email removal
- Rejected-record export with reasons
- JSON data quality report

## Tech Stack
- Python 3
- Pandas
- CSV
- JSON

## Project Files
- `main.py` — data cleaning logic
- `sample_companies.csv` — sample input data
- `cleaned_companies.csv` — valid, deduplicated records
- `rejected_companies.csv` — records requiring review
- `report.json` — processing summary
- `requirements.txt` — Python dependencies

## How to Run

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python3 main.py
```

## Sample Results
- Input records: 8
- Cleaned records: 4
- Rejected records: 3
- Duplicate records removed: 1

## Limitations
Email validation checks format only. It does not verify
whether an email address exists or can receive messages.

## Learning Outcomes
This project demonstrates beginner-level data ingestion,
validation, cleaning, deduplication, and reporting.
