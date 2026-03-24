# src/visualiser.py
import matplotlib.pyplot as plt
import os

def generate_visualisations(ticker, df, output_dir):
    """
    Creates financial charts and saves them as PNGs.
    """
    plot_dir = os.path.join(output_dir, "visualisations")
    os.makedirs(plot_dir, exist_ok=True)
    
    # --- 1. Revenue vs Net Income Trend (Line Chart) ---
    if 'Total Revenue' in df.columns and 'Net Income' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['Total Revenue'], marker='o', label='Total Revenue', color='#1f77b4')
        plt.plot(df.index, df['Net Income'], marker='s', label='Net Income', color='#ff7f0e')
        
        plt.title(f"{ticker}: Revenue vs Net Income Trend (Millions)")
        plt.xlabel("Date")
        plt.ylabel("Value (Millions)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.savefig(os.path.join(plot_dir, "revenue_profit_trend.png"))
        plt.close()

    # --- 2. Capital Structure (Debt vs Equity Bar Chart) ---
    if 'Total Liabilities' in df.columns and 'Stockholders Equity' in df.columns:
        # Get the latest data point
        latest = df.iloc[-1]
        labels = ['Liabilities', 'Equity']
        values = [latest['Total Liabilities'], latest['Stockholders Equity']]
        
        plt.figure(figsize=(8, 6))
        plt.bar(labels, values, color=['#d62728', '#2ca02c'])
        
        plt.title(f"{ticker}: Capital Structure (Latest)")
        plt.ylabel("Value (Millions)")
        
        plt.savefig(os.path.join(plot_dir, "capital_structure.png"))
        plt.close()

    # --- 3. NEW: Margin Heatmap ---
    margin_cols = [c for c in ['Gross Margin (%)', 'Net Margin (%)'] if c in df.columns]
    if margin_cols:
        data = df[margin_cols].T # Transpose to get years on X-axis
        
        plt.figure(figsize=(10, 4))
        plt.imshow(data, cmap='RdYlGn', aspect='auto')
        
        # Add labels
        plt.colorbar(label='Percentage (%)')
        plt.xticks(range(len(df.index)), [d.strftime('%Y') for d in df.index])
        plt.yticks(range(len(margin_cols)), margin_cols)
        plt.title(f"{ticker}: Margin Expansion/Contraction")
        
        # Annotate values on the "heatmap"
        for i in range(len(margin_cols)):
            for j in range(len(df.index)):
                plt.text(j, i, f"{data.iloc[i, j]:.1f}%", ha='center', va='center', color='black')

        plt.savefig(os.path.join(plot_dir, "margin_heatmap.png"))
        plt.close()

    return plot_dir