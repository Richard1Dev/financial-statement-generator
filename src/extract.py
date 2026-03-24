import yfinance as yf

def get_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # .financials, .balance_sheet, .cashflow return DataFrames
    return {
        "income": stock.financials,
        "balance": stock.balance_sheet,
        "cash": stock.cashflow
    }
