# src/transform.py
import pandas as pd

def calculate_insights(data_dict):
    # 1. Transpose and Immediately name the Index
    df_inc = data_dict['income'].T
    df_inc.index.name = 'Date'
    
    df_bal = data_dict['balance'].T
    df_bal.index.name = 'Date'
    
    df_cf = data_dict['cash'].T
    df_cf.index.name = 'Date'

    # Sort by date so YoY and trends move forward in time
    df_inc = df_inc.sort_index()
    df_bal = df_bal.sort_index()
    df_cf = df_cf.sort_index()

    # 2. Expanded Accountant's 'Vital Signs' 
    # Adding Gross Profit and Total Debt gives a better picture of health
    target_cols = [
        'Total Revenue', 'Gross Profit', 'Net Income', 
        'Total Assets', 'Total Liabilities', 'Total Debt',
        'Current Assets', 'Current Liabilities', 'Free Cash Flow'
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()

    # 3. Calculations (YoY and Ratios)
    if 'Total Revenue' in condensed:
        condensed['Revenue Growth (%)'] = condensed['Total Revenue'].pct_change() * 100
    
    if 'Net Income' in condensed and 'Total Revenue' in condensed:
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100

    if 'Current Assets' in condensed and 'Current Liabilities' in condensed:
        condensed['Current Ratio'] = condensed['Current Assets'] / condensed['Current Liabilities']

    # 4. Generate Executive Summary Text
    latest = condensed.iloc[-1]
    name = data_dict['metadata']['name']
    curr = data_dict['metadata']['currency']
    
    summary_text = f"FINANCIAL REPORT: {name}\n"
    summary_text += f"Currency: {curr} | Denominated in Millions (where applicable)\n"
    summary_text += "="*40 + "\n"
    
    # Simple logic-based insights for the accountant
    if 'Net Margin (%)' in latest:
        margin = latest['Net Margin (%)']
        summary_text += f"- Profitability: Net Margin is {margin:.2f}%\n"
        
    if 'Current Ratio' in latest:
        cr = latest['Current Ratio']
        desc = "Strong" if cr > 1.5 else "Adequate" if cr >= 1.0 else "Weak"
        summary_text += f"- Liquidity: {desc} (Current Ratio: {cr:.2f})\n"

    # 5. Denominate specific monetary columns in Millions
    # We DON'T divide the percentages or the ratios
    monetary_cols = [
        'Total Revenue', 'Gross Profit', 'Net Income', 
        'Total Assets', 'Total Liabilities', 'Total Debt', 
        'Current Assets', 'Current Liabilities', 'Free Cash Flow'
    ]
    
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    return {
        "report": condensed.dropna(how='all'),
        "text_summary": summary_text
    }