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
    target_cols = [
        'Total Revenue', 'Net Income', 'Total Assets', 
        'Total Liabilities Net Minority Interest', 'Stockholders Equity',
        'Current Assets', 'Current Liabilities', 'Free Cash Flow',
        'Inventory', 'Receivables' 
    ]
    
    combined = pd.concat([df_inc, df_bal, df_cf], axis=1)
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed = combined[available_cols].copy()
    condensed.rename(columns={'Total Liabilities Net Minority Interest': 'Total Liabilities'}, inplace=True)

    # --- CALCULATIONS ---
    latest_row = condensed.iloc[-1]
    
    # Integrity Check
    assets = latest_row.get('Total Assets', 0)
    liabs = latest_row.get('Total Liabilities', 0)
    equity = latest_row.get('Stockholders Equity', 0)
    imbalance = abs(assets - (liabs + equity))
    integrity_passed = imbalance < 1000000 
    integrity_msg = "PASSED" if integrity_passed else f"FAILED (Diff: {imbalance:,.0f})"

    # Ratios & Growth
    if 'Total Revenue' in condensed:
        condensed['Rev Growth (%)'] = condensed['Total Revenue'].pct_change() * 100
        condensed['Net Margin (%)'] = (condensed['Net Income'] / condensed['Total Revenue']) * 100
        
        # Cash Cycle
        inv = condensed.get('Inventory', 0).fillna(0)
        rec = condensed.get('Receivables', 0).fillna(0)
        condensed['Cash Cycle (Days)'] = ((inv + rec) / condensed['Total Revenue']) * 365

    if 'Current Assets' in condensed and 'Current Liabilities' in condensed:
        condensed['Current Ratio'] = condensed['Current Assets'] / condensed['Current Liabilities']
    
    # Debt Ratio (Leverage)
    if 'Total Liabilities' in condensed and 'Total Assets' in condensed:
        condensed['Debt Ratio'] = condensed['Total Liabilities'] / condensed['Total Assets']

    # --- EXECUTIVE INSIGHTS GENERATION ---
    name = data_dict['metadata']['name']
    summary = [f"FINANCIAL ANALYSER EXECUTIVE SUMMARY: {name}", f"Integrity Check: {integrity_msg}", "="*50]

    # Leverage Insight
    if 'Debt Ratio' in condensed.columns:
        dr = latest_row.get('Debt Ratio', 0)
        risk = "HIGH" if dr > 0.7 else "MODERATE" if dr > 0.4 else "LOW"
        summary.append(f"- LEVERAGE: {risk} (Debt Ratio: {dr:.2f}).")
        if dr > 0.7: summary.append("  [!] Warning: High reliance on debt financing.")

    # Profitability Insight
    if 'Net Margin (%)' in condensed.columns:
        nm = latest_row.get('Net Margin (%)', 0)
        perf = "STRONG" if nm > 15 else "HEALTHY" if nm > 5 else "THIN"
        summary.append(f"- PROFITABILITY: {perf} (Net Margin: {nm:.2f}%).")

    # Liquidity Insight
    if 'Current Ratio' in condensed.columns:
        cr = latest_row.get('Current Ratio', 0)
        liq = "SOLVENT" if cr > 1.2 else "CRITICAL"
        summary.append(f"- LIQUIDITY: {liq} (Current Ratio: {cr:.2f}).")

    # Efficiency Insight
    if 'Cash Cycle (Days)' in condensed.columns:
        cc = latest_row.get('Cash Cycle (Days)', 0)
        summary.append(f"- EFFICIENCY: {cc:.1f} days to convert operations to cash.")

    # --- FINAL CLEANUP ---
    condensed.drop(columns=['Inventory', 'Receivables'], inplace=True, errors='ignore')
    monetary_cols = ['Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities', 'Stockholders Equity', 'Free Cash Flow', 'Current Assets', 'Current Liabilities']
    for col in monetary_cols:
        if col in condensed.columns:
            condensed[col] = (condensed[col] / 1_000_000).round(2)

    return {
        "report": condensed.dropna(how='all').round(2),
        "text_summary": "\n".join(summary),
        "integrity": integrity_msg
    }