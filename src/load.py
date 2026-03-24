# src/load.py
import os
from datetime import datetime

def save_to_csv(ticker, transformed_data):
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "outputs", f"{ticker}_report")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Save main report
    report_path = os.path.join(output_dir, "main_report.csv")
    transformed_data['report'].to_csv(report_path)

    # 2. Save Executive Summary
    summary_path = os.path.join(output_dir, "executive_summary.txt")
    with open(summary_path, "w") as f:
        f.write(transformed_data['text_summary'])

    # 3. Save Audit Log
    audit_path = os.path.join(output_dir, "audit_log.txt")
    with open(audit_path, "w") as f:
        f.write(f"REPORT AUDIT LOG\n")
        f.write(f"----------------\n")
        f.write(f"Ticker: {ticker}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Data Source: Yahoo Finance\n")
        f.write(f"Integrity Check: {transformed_data['integrity']}\n")

    return output_dir