# src/main.py
from extract import get_data
from transform import calculate_insights
from load import save_to_csv
import sys

def run_pipeline(ticker, quarterly):
    try:
        print(f"\n--- Initialising Analysis for {ticker} ---")
        
        # 1. Extract
        raw_data = get_data(ticker, quarterly)
        
        # Validation: yf.Ticker doesn't always fail on bad symbols, 
        # but the dataframes will be empty.
        if raw_data['income'].empty:
            raise ValueError(f"No financial data found for '{ticker}'. Check the symbol.")

        # 2. Transform
        clean_data = calculate_insights(raw_data)
        
        # 3. Load
        path = save_to_csv(ticker, clean_data)
        
        print(f"SUCCESS: Report generated in British English.")
        print(f"LOCATION: {path}")

    except Exception as e:
        print(f"\nERROR: Could not process {ticker}.")
        print(f"REASON: {e}")
        # Suggesting a restart rather than a hard crash
        return

if __name__ == "__main__":
    print("=== Financial Statement Generator ===")
    symbol = input("Enter Ticker (e.g., AAPL, TSLA, BP.L): ").upper().strip()
    
    period_choice = input("Report Type - [A]nnual or [Q]uarterly? ").upper().strip()
    is_quarterly = True if period_choice == 'Q' else False
    
    run_pipeline(symbol, is_quarterly)