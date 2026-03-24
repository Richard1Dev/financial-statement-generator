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

    # 2. Extract specific columns for our Accountant's Table
    # We use a 'target' list to keep the report from getting too wide
    target_cols = [
        'Total Revenue', 'Gross Profit', 'Net Income', 
        'Total Assets', 'Total Liabilities Net Minority Interest', 
        'Stockholders Equity', 'Inventory', 'Receivables', 
        'Current Assets', 'Current Liabilities', 'Free Cash Flow'
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()

    # 3. Validation Check: Do Assets = Liabilities + Equity?
    # We check the most recent period (last row)
    latest_row = condensed.iloc[-1]
    assets = latest_row.get('Total Assets', 0)
    liabs = latest_row.get('Total Liabilities Net Minority Interest', 0)
    equity = latest_row.get('Stockholders Equity', 0)
    
    # We allow a small margin (100,000) for rounding differences in large corps
    imbalance = abs(assets - (liabs + equity))
    integrity_passed = imbalance < 100000
    integrity_msg = "PASSED" if integrity_passed else f"FAILED (Diff: {imbalance:,.0f})"

    # 4. Calculations: YoY and Ratios
    if 'Total Revenue' in condensed:
        condensed['Revenue Growth (%)'] = condensed['Total Revenue'].pct_change() * 100
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100

    if 'Current Assets' in condensed and 'Current Liabilities' in condensed:
        condensed['Current Ratio'] = condensed['Current Assets'] / condensed['Current Liabilities']

    # 5. Generate Executive Summary Text
    name = data_dict['metadata']['name']
    curr = data_dict['metadata']['currency']
    
    summary_text = f"FINANCIAL ANALYSER REPORT: {name}\n"
    summary_text += f"Currency: {curr} | Integrity Check: {integrity_msg}\n"
    summary_text += "="*50 + "\n"
    
    if not integrity_passed:
        summary_text += "WARNING: Balance sheet does not balance. Use data with caution.\n\n"

    if 'Net Margin (%)' in latest_row:
        summary_text += f"- Profitability: {latest_row['Net Margin (%)']:.2f}% Net Margin\n"
    
    if 'Current Ratio' in latest_row:
        summary_text += f"- Liquidity: {latest_row['Current Ratio']:.2f} Current Ratio\n"

    # 6. Final Formatting (Millions)
    # List of columns that represent currency values
    monetary_cols = [
        'Total Revenue', 'Gross Profit', 'Net Income', 'Total Assets', 
        'Total Liabilities Net Minority Interest', 'Stockholders Equity', 
        'Inventory', 'Free Cash Flow', 'Current Assets', 'Current Liabilities'
    ]
    
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    return {
        "report": condensed.dropna(how='all').round(2),
        "text_summary": summary_text,
        "integrity": integrity_msg
    }