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
    target_cols = [
        'Total Revenue', 'Gross Profit', 'Net Income', 
        'Total Assets', 'Inventory', 'Receivables', 'Accounts Payable',
        'Current Assets', 'Current Liabilities', 'Free Cash Flow'
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()

    # 3. Calculations: Common Size (% of Revenue)
    if 'Total Revenue' in condensed:
        condensed['Gross Margin (%)'] = (condensed['Gross Profit'] / condensed['Total Revenue']) * 100
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100

    # 4. Calculations: Cash Conversion Cycle (CCC)
    # CCC = DIO + DSO - DPO (Days Inventory + Days Sales Out - Days Payables Out)
    if 'Total Revenue' in condensed:
        # We assume 365 days for the calculation
        if 'Inventory' in condensed:
            condensed['Days Inventory'] = (condensed['Inventory'] / condensed['Total Revenue']) * 365
        if 'Receivables' in condensed:
            condensed['Days Sales Out'] = (condensed['Receivables'] / condensed['Total Revenue']) * 365
        
        # Simple CCC estimation
        cols_for_ccc = ['Days Inventory', 'Days Sales Out']
        if all(col in condensed for col in cols_for_ccc):
            condensed['Cash Conversion Cycle (Days)'] = condensed['Days Inventory'] + condensed['Days Sales Out']

    # 5. Executive Summary Text Update
    latest = condensed.iloc[-1]
    name = data_dict['metadata']['name']
    summary_text = f"FINANCIAL ANALYSER REPORT: {name}\n"
    summary_text += "="*40 + "\n"
    
    if 'Cash Conversion Cycle (Days)' in latest:
        ccc = latest['Cash Conversion Cycle (Days)']
        summary_text += f"- Operational Efficiency: Cash cycle is {ccc:.1f} days.\n"
    
    if 'Net Margin (%)' in latest:
        summary_text += f"- Profitability: {latest['Net Margin (%)']:.2f}% Net Margin.\n"

    # 6. Final Formatting (Millions)
    monetary_cols = ['Total Revenue', 'Gross Profit', 'Net Income', 'Total Assets', 'Inventory', 'Free Cash Flow']
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    return {
        "report": condensed.dropna(how='all').round(2),
        "text_summary": summary_text
    }