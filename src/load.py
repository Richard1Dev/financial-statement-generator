import os

def save_to_csv(ticker, transformed_data):
    output_dir = f"../outputs/{ticker}_report"
    os.makedirs(output_dir, exist_ok=True)
    
    for name, df in transformed_data.items():
        df.to_csv(f"{output_dir}/{name}.csv")
    return output_dir
