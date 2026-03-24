# src/load.py
import os
from datetime import datetime

def save_to_csv(ticker, transformed_data):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "outputs", f"{ticker}_report")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the main CSV
    transformed_data['report'].to_csv(os.path.join(output_dir, "main_report.csv"))

    # 3a. Save Executive Summary
    with open(os.path.join(output_dir, "executive_summary.txt"), "w") as f:
        f.write(transformed_data['text_summary'])

    # 3c. Audit Log
    with open(os.path.join(output_dir, "audit_log.txt"), "w") as f:
        f.write(f"Data fetched at: {datetime.now()}\n")
        f.write(f"Source: Yahoo Finance via yfinance\n")
        f.write(f"Ticker: {ticker}\n")

    return output_dir