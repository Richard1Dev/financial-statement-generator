# Financial Statement Analyser

A professional-grade Python tool designed for accountants and financial analysts. This tool automates the extraction of company data via Yahoo Finance, applies standard accounting transformations, and generates high-density reports, executive summaries, and visualisations.

---

## Key Features

### 1. Advanced Financial Transformations (The 'T' in ETL)
- **Common Size Analysis:** Automatic calculation of Net Margins and Revenue Growth.
- **Liquidity & Solvency:** Real-time tracking of Current Ratios and Debt-to-Asset leverage.
- **Operational Efficiency:** Calculation of the **Cash Conversion Cycle (Days)**.
- **Data Integrity Check:** Automated validation of the fundamental accounting equation:  
  $$Total Assets = Total Liabilities + Stockholders' Equity$$

### 2. Batch Processing & Peer Comparison
- **Multi-Ticker Support:** Process an entire sector (e.g., `BP.L, SHEL.L, TTE.PA`) in one command.
- **Sector Comparison:** Generates a `Sector_Comparison.csv` capturing the latest "Vital Signs" across all processed tickers for instant benchmarking.

### 3. Professional Outputs
- **Executive Summaries:** Human-readable `.txt` insights flagging "High Leverage" or "Strong Profitability."
- **Visualisation Suite:** Automated PNG charts for Revenue/Profit trends and Capital Structure (Debt vs. Equity).
- **Audit Logging:** Full transparency with timestamped logs and data source verification.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Richard1Dev/financial-analyser.git](https://github.com/Richard1Dev/financial-analyser.git)
   cd financial-analyser
   ```

2. **Install dependencies:**
   ```bash
   pip install yfinance pandas matplotlib
   ```

---

## Usage

Run the main script from the root directory:

```bash
python src/main.py
```

1. **Enter Tickers:** Provide a single ticker (e.g., `AAPL`) or a list (`TSLA, MSFT, GOOG`).
2. **Choose Period:** Select **[A]** for Annual reports or **[Q]** for Quarterly insights.
3. **Review Outputs:** Check the `outputs/` folder for individual company directories and the master comparison file.

---

## Project Structure

- `src/extract.py`: Handles raw data fetching and currency detection.
- `src/transform.py`: The "Brain" – applies accounting logic and risk assessment.
- `src/visualiser.py`: Generates trend lines and capital structure bars.
- `src/load.py`: Manages file I/O and audit logging.
- `src/main.py`: Orchestrates the batch processing loop.

---

## Disclaimer
This tool is for educational and informational purposes only. It is not financial advice. All data is sourced via the `yfinance` library.
