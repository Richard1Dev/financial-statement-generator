# src/main.py
# src/main.py
from extract import get_data
from transform import calculate_insights
from load import save_to_csv
import sys

def run_pipeline(ticker, quarterly):
    try:
        # 1. Extract
        raw_data = get_data(ticker, quarterly)
        
        # Validation: check if yfinance actually returned anything
        if raw_data['income'].empty:
            print(f"  [!] No data found for {ticker}. Skipping...")
            return

        # 2. Transform
        clean_data = calculate_insights(raw_data)
        
        # 3. Load
        path = save_to_csv(ticker, clean_data)
        print(f"  [+] Success: {ticker} report saved to {path}")

    except Exception as e:
        print(f"  [!] Error processing {ticker}: {e}")

if __name__ == "__main__":
    print("=== British Financial Statement Analyser (Batch Mode) ===")
    
    # Multi-ticker input
    user_input = input("Enter Ticker(s) separated by commas (e.g. AAPL, TSLA, BP.L): ")
    tickers = [t.strip().upper() for t in user_input.split(',')]
    
    # Period Choice
    period_choice = input("Report Type - [A]nnual or [Q]uarterly? ").upper().strip()
    is_quarterly = True if period_choice == 'Q' else False
    
    print(f"\nProcessing {len(tickers)} ticker(s)...\n")
    
    # The Loop
    for symbol in tickers:
        print(f"Analysing {symbol}...")
        run_pipeline(symbol, is_quarterly)
        
    print("\n=== Batch Processing Complete ===")