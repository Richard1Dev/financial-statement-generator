# src/main.py
from extract import get_data
from transform import calculate_insights
from load import save_to_csv
from visualiser import generate_visualisations
import pandas as pd
import os

def run_pipeline(ticker, quarterly):
    try:
        raw_data = get_data(ticker, quarterly)
        if raw_data['income'].empty:
            print(f"  [!] No data found for {ticker}. Skipping...")
            return None

        clean_data = calculate_insights(raw_data)
        path = save_to_csv(ticker, clean_data)
        generate_visualisations(ticker, clean_data['report'], path)
        print(f"  [+] Success: {ticker} report saved to {path}")
        
        # Get the most recent row for the comparison table
        latest_stats = clean_data['report'].iloc[-1:].copy()
        latest_stats.index = [ticker] 
        return latest_stats

    except Exception as e:
        print(f"  [!] Error processing {ticker}: {e}")
        return None

if __name__ == "__main__":
    print("=== Financial Statement Analyser (Batch Mode) ===")
    
    user_input = input("Enter Ticker(s) separated by commas (e.g. AAPL, TSLA, BP.L): ")
    tickers = [t.strip().upper() for t in user_input.split(',')]
    
    period_choice = input("Report Type - [A]nnual or [Q]uarterly? ").upper().strip()
    is_quarterly = True if period_choice == 'Q' else False
    
    comparison_results = []
    
    print(f"\nProcessing {len(tickers)} ticker(s)...\n")
    
    for symbol in tickers:
        print(f"Analysing {symbol}...")
        result = run_pipeline(symbol, is_quarterly)
        if result is not None:
            comparison_results.append(result)
            
    # Generate the Comparison CSV
    if len(comparison_results) > 1:
        print("\nGenerating Sector Comparison...")
        comparison_df = pd.concat(comparison_results)
        
        # Give the index a name so it doesn't show up as 'Unnamed: 0'
        comparison_df.index.name = 'Ticker'
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Standardised capitalised filename
        comp_path = os.path.join(base_dir, "outputs", "Sector_Comparison.csv")
        
        comparison_df.to_csv(comp_path)
        print(f"  [>>>] Sector Comparison saved to: {comp_path}")
        
    print("\n=== Batch Processing Complete ===")