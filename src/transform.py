# src/transform.py
import pandas as pd

def calculate_insights(data_dict):
    df_inc = data_dict['income'].T
    df_bal = data_dict['balance'].T
    df_cf = data_dict['cash'].T
    
    for df in [df_inc, df_bal, df_cf]:
        df.index.name = 'Date'
        df.sort_index(inplace=True)

    target_cols = [
        'Total Revenue', 'Net Income', 'Total Assets', 
        'Total Liabilities Net Minority Interest', 'Stockholders Equity',
        'Current Assets', 'Current Liabilities', 'Free Cash Flow',
        'Inventory', 'Receivables', 'Gross Profit'
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()
    condensed.rename(columns={'Total Liabilities Net Minority Interest': 'Total Liabilities'}, inplace=True)

    # --- CALCULATIONS (Perform these BEFORE creating latest_row) ---
    if 'Total Revenue' in condensed:
        condensed['Rev Growth (%)'] = condensed['Total Revenue'].pct_change() * 100
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100
        if 'Gross Profit' in condensed:
            condensed['Gross Margin (%)'] = (condensed['Gross Profit'] / condensed['Total Revenue']) * 100
        
        inv = condensed.get('Inventory', 0).fillna(0)
        rec = condensed.get('Receivables', 0).fillna(0)
        condensed['Cash Cycle (Days)'] = ((inv + rec) / condensed['Total Revenue']) * 365

    if 'Current Assets' in condensed and 'Current Liabilities' in condensed:
        condensed['Current Ratio'] = condensed['Current Assets'] / condensed['Current Liabilities']
    
    if 'Total Liabilities' in condensed and 'Total Assets' in condensed:
        condensed['Debt Ratio'] = condensed['Total Liabilities'] / condensed['Total Assets']

    # NOW capture the latest row for the summary
    latest_row = condensed.iloc[-1]

    # --- EXECUTIVE INSIGHTS ---
    name = data_dict['metadata']['name']
    
    # Integrity Check
    imbalance = abs(latest_row.get('Total Assets', 0) - (latest_row.get('Total Liabilities', 0) + latest_row.get('Stockholders Equity', 0)))
    integrity_msg = "PASSED" if imbalance < 1000000 else "FAILED"

    summary = [f"FINANCIAL ANALYSER EXECUTIVE SUMMARY: {name}", f"Integrity Check: {integrity_msg}", "="*50]

    if 'Debt Ratio' in condensed.columns:
        dr = latest_row['Debt Ratio']
        risk = "HIGH" if dr > 0.7 else "MODERATE" if dr > 0.4 else "LOW"
        summary.append(f"- LEVERAGE: {risk} (Debt Ratio: {dr:.2f}).")

    if 'Net Margin (%)' in condensed.columns:
        nm = latest_row['Net Margin (%)']
        perf = "STRONG" if nm > 15 else "HEALTHY" if nm > 5 else "THIN"
        summary.append(f"- PROFITABILITY: {perf} (Net Margin: {nm:.2f}%).")

    if 'Current Ratio' in condensed.columns:
        cr = latest_row['Current Ratio']
        liq = "SOLVENT" if cr > 1.2 else "CRITICAL"
        summary.append(f"- LIQUIDITY: {liq} (Current Ratio: {cr:.2f}).")

    # --- CLEANUP ---
    # We keep Gross Margin and Net Margin for the Heatmap/Visualiser
    monetary_cols = ['Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities', 'Stockholders Equity', 'Free Cash Flow', 'Current Assets', 'Current Liabilities']
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    return {
        "report": condensed.dropna(how='all').round(2),
        "text_summary": "\n".join(summary),
        "integrity": integrity_msg
    }