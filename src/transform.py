import pandas as pd

def calculate_insights(data_dict):
    # 1. Transpose
    df_inc = data_dict['income'].T
    df_bal = data_dict['balance'].T
    df_cfl = data_dict['cash'].T
    
    df_inc.index.name = 'Date'
    df_bal.index.name = 'Date'
    df_cfl.index.name = 'Date'

    # 2. Accountant's 'Vital Signs' (The only columns we actually want)
    # We use .get() or list intersection to avoid errors if a row is missing
    target_cols = [
        'Total Revenue', 'Gross Profit', 'Operating Income', 
        'Net Income', 'Total Assets', 'Total Liabilities', 
        'Free Cash Flow', 'Total Debt'
    ]
    
    # Combine all statements into one big table to filter easily
    combined = pd.concat([df_inc, df_bal, df_cfl], axis=1)
    
    # Filter to only the columns that exist in the data
    available_cols = [c for c in target_cols if c in combined.columns]
    condensed_df = combined[available_cols].copy()

    # 3. Calculate Key Ratios (The 'Insights')
    insights = pd.DataFrame(index=condensed_df.index)
    
    if 'Net Income' in condensed_df and 'Total Revenue' in condensed_df:
        insights['Net Profit Margin'] = condensed_df['Net Income'] / condensed_df['Total Revenue']
    
    if 'Total Liabilities' in condensed_df and 'Total Assets' in condensed_df:
        insights['Debt Ratio'] = condensed_df['Total Liabilities'] / condensed_df['Total Assets']

    # 4. Final Polish: Denominate financial values in Millions
    # Only apply to the raw dollar values, not the ratios
    monetary_cols = condensed_df.columns
    condensed_df[monetary_cols] = condensed_df[monetary_cols] / 1_000_000

    return {
        "summary_statement_millions": condensed_df.round(2),
        "key_ratios": insights.round(4)
    }