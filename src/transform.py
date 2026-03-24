def calculate_insights(data_dict):
    # Transpose so dates are rows
    df_inc = data_dict['income'].T
    df_bal = data_dict['balance'].T
    df_cfl = data_dict['cash'].T

    df_inc.index.name = 'Date'
    df_bal.index.name = 'Date'
    df_cfl.index.name = 'Date'
    
    # Quick Insight: Net Profit Margin
    # Standardize column names to lowercase/no spaces if yfinance varies
    insights = df_inc[['Net Income', 'Total Revenue']].copy()
    insights['Profit Margin'] = insights['Net Income'] / insights['Total Revenue']
    
    return {
        "income_statement": df_inc,
        "balance_sheet": df_bal,
        "cash_flow": df_cfl,
        "insights": insights
    }
