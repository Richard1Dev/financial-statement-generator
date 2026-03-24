import os

def save_to_csv(ticker, transformed_data):
    # Use absolute pathing to ensure it finds /outputs/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "outputs", f"{ticker}_report")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for name, df in transformed_data.items():
        # Saving with index=True because the Date is our Index
        df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=True)
        
    return output_dir
