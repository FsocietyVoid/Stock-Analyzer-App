# Stock Risk Analyzer

## Overview
Stock Risk Analyzer is a desktop application designed to assess the risk of stock investments using key financial metrics. The application provides risk analysis based on historical stock data, helping investors make informed decisions.

## Features
- Fetches real-time stock data from Yahoo Finance.
- Calculates key risk metrics such as:
  - **Value at Risk (VaR 95%)** – Measures the worst expected loss at a 95% confidence level.
  - **Conditional VaR (CVaR 95%)** – Estimates potential extreme losses beyond VaR.
  - **Volatility** – Assesses the overall price fluctuations of the stock.
  - **Sharpe Ratio** – Evaluates risk-adjusted returns.
  - **Sortino Ratio** – Similar to Sharpe Ratio but focuses on downside risk.
  - **Maximum Drawdown** – Identifies the worst peak-to-trough decline.
- Provides an investment decision recommendation based on risk metrics.
- Allows users to save the analysis results as a CSV file.

## Technology Stack
- **Python** – Core programming language
- **Tkinter** – GUI framework for the desktop application
- **Yahoo Finance API (yfinance)** – Fetching real-time stock data
- **NumPy & Pandas** – Data processing and financial calculations

## Installation
### Prerequisites
Ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).

### Install Dependencies
Run the following command to install required libraries:
```sh
pip install yfinance numpy pandas tkinter
```

### Running the Application
```sh
python stock_analyzer.py
```

## Usage
1. Enter the stock ticker symbol (e.g., AAPL, TSLA, MSFT) into the input field.
2. Click the "Analyze" button to fetch and calculate risk metrics.
3. View the generated investment insights.
4. Save results as a CSV file for further analysis.

## Limitations
- The application relies on historical stock data and statistical risk models, which may not always predict future market conditions accurately.
- It does not consider macroeconomic factors or qualitative financial data.

## License
This project is licensed under the MIT License.

