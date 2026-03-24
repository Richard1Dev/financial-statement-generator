# src/extract.py
import yfinance as yf

def get_data(ticker_symbol, quarterly=False):
    stock = yf.Ticker(ticker_symbol)
    
    if quarterly:
        income = stock.quarterly_financials
        balance = stock.quarterly_balance_sheet
        cash = stock.quarterly_cashflow
    else:
        income = stock.financials
        balance = stock.balance_sheet
        cash = stock.cashflow

    info = stock.info
    metadata = {
        "currency": info.get("currency", "Unknown"),
        "name": info.get("longName", "Unknown Company")
    }

    return {
        "income": income,
        "balance": balance,
        "cash": cash,
        "metadata": metadata
    }