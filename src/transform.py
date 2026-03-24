# src/transform.py
import pandas as pd

def calculate_insights(data_dict):
    # 1. Transpose and Name Index
    df_inc = data_dict['income'].T
    df_bal = data_dict['balance'].T
    df_cf = data_dict['cash'].T
    
    for df in [df_inc, df_bal, df_cf]:
        df.index.name = 'Date'
        df.sort_index(inplace=True)

    # 2. Extract specific columns
    # We use 'Total Liabilities Net Minority Interest' as the source but will rename it
    target_cols = [
        'Total Revenue', 'Net Income', 'Total Assets', 
        'Total Liabilities Net Minority Interest', 'Stockholders Equity',
        'Current Assets', 'Current Liabilities', 'Free Cash Flow',
        'Inventory', 'Receivables' 
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()

    # --- RENAME VERBOSE COLUMNS ---
    rename_map = {'Total Liabilities Net Minority Interest': 'Total Liabilities'}
    condensed.rename(columns=rename_map, inplace=True)

    # --- CALCULATIONS ---
    # Integrity Check
    latest_row = condensed.iloc[-1]
    assets = latest_row.get('Total Assets', 0)
    liabs = latest_row.get('Total Liabilities', 0)
    equity = latest_row.get('Stockholders Equity', 0)
    
    imbalance = abs(assets - (liabs + equity))
    integrity_msg = "PASSED" if imbalance < 1000000 else "FAILED"

    # Growth and Margins
    if 'Total Revenue' in condensed:
        condensed['Rev Growth (%)'] = condensed['Total Revenue'].pct_change() * 100
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100

    # Cash Cycle (Days) - Using .fillna(0) for companies without inventory
    if 'Total Revenue' in condensed:
        inv = condensed.get('Inventory', 0).fillna(0)
        rec = condensed.get('Receivables', 0).fillna(0)
        condensed['Cash Cycle (Days)'] = ((inv + rec) / condensed['Total Revenue']) * 365

    # Liquidity
    if 'Current Assets' in condensed and 'Current Liabilities' in condensed:
        condensed['Current Ratio'] = condensed['Current Assets'] / condensed['Current Liabilities']

    # --- CLEANUP ---
    # Drop raw 'helper' columns to save horizontal space
    condensed.drop(columns=['Inventory', 'Receivables'], inplace=True, errors='ignore')

    # Formatting monetary values to Millions
    monetary_cols = [
        'Total Revenue', 'Net Income', 'Total Assets', 
        'Total Liabilities', 'Stockholders Equity', 
        'Free Cash Flow', 'Current Assets', 'Current Liabilities'
    ]
    
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    # Text Summary Generation
    name = data_dict['metadata']['name']
    summary_text = f"FINANCIAL ANALYSER REPORT: {name}\n"
    summary_text += f"Integrity Check: {integrity_msg}\n"
    summary_text += "="*45 + "\n"
    
    if 'Net Margin (%)' in latest_row:
        summary_text += f"- Profitability: {latest_row['Net Margin (%)']:.2f}% Net Margin\n"
    if 'Cash Cycle (Days)' in latest_row:
        summary_text += f"- Efficiency: {latest_row['Cash Cycle (Days)']:.1f} day Cash Cycle\n"

    return {
        "report": condensed.dropna(how='all').round(2),
        "text_summary": summary_text,
        "integrity": integrity_msg
    }