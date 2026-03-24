from extract import get_data
from transform import calculate_insights
from load import save_to_csv

def run_pipeline(ticker):
    print(f"Processing {ticker}...")
    raw_data = get_data(ticker)
    clean_data = calculate_insights(raw_data)
    path = save_to_csv(ticker, clean_data)
    print(f"Success! Files saved to: {path}")

if __name__ == "__main__":
    symbol = input("Enter Ticker: ").upper()
    run_pipeline(symbol)
