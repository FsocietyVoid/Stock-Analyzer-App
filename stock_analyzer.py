import sys

class DummyFile:
    def write(self, x): pass
    def flush(self): pass  # This ensures flush() method is present

sys.stdout = DummyFile()
sys.stderr = DummyFile()


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yfinance as yf
import numpy as np
import pandas as pd

# Define Colors
BG_COLOR = "#1e1e2e"
CARD_COLOR = "#2a2a3b"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#ffcc00"

# Create Main Window
root = tk.Tk()
root.title("Stock Risk Analyzer")
root.geometry("600x700")
root.configure(bg=BG_COLOR)

# Title Label
title_label = tk.Label(root, text="📈 Stock Risk Analyzer", font=("Helvetica", 18, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
title_label.pack(pady=10)

# Stock Input
input_frame = tk.Frame(root, bg=CARD_COLOR, bd=2, relief="ridge")
input_frame.pack(pady=10, padx=20, fill="x")

stock_label = tk.Label(input_frame, text="Enter Stock Ticker:", font=("Helvetica", 12, "bold"), fg=TEXT_COLOR, bg=CARD_COLOR)
stock_label.pack(pady=5)

stock_entry = tk.Entry(input_frame, font=("Helvetica", 12), justify="center", width=15, bg="#3b3b4f", fg=TEXT_COLOR, relief="solid")
stock_entry.pack(pady=5)

# Grid for Risk Metrics
grid_frame = tk.Frame(root, bg=BG_COLOR)
grid_frame.pack(pady=10)

# Create 6 Text Variables
var_text = tk.StringVar()
cvar_text = tk.StringVar()
volatility_text = tk.StringVar()
sharpe_text = tk.StringVar()
sortino_text = tk.StringVar()
drawdown_text = tk.StringVar()
decision_text = tk.StringVar()

# Function to create metric boxes in grid
def create_info_box(parent, title, value_var, row, col):
    frame = tk.Frame(parent, bg=CARD_COLOR, bd=2, relief="ridge")
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    tk.Label(frame, text=title, font=("Helvetica", 12, "bold"), fg=ACCENT_COLOR, bg=CARD_COLOR).pack(pady=3)
    tk.Label(frame, textvariable=value_var, font=("Helvetica", 12), fg=TEXT_COLOR, bg=CARD_COLOR).pack(pady=3)

# Place each metric in a 3x2 grid
create_info_box(grid_frame, "🔻 VaR (95%)", var_text, 0, 0)
create_info_box(grid_frame, "📉 CVaR (95%)", cvar_text, 0, 1)
create_info_box(grid_frame, "📊 Volatility", volatility_text, 0, 2)
create_info_box(grid_frame, "⚖️ Sharpe Ratio", sharpe_text, 1, 0)
create_info_box(grid_frame, "📉 Sortino Ratio", sortino_text, 1, 1)
create_info_box(grid_frame, "📉 Max Drawdown", drawdown_text, 1, 2)

# Investment Decision Box
decision_frame = tk.Frame(root, bg=CARD_COLOR, bd=2, relief="ridge")
decision_frame.pack(pady=10, padx=20, fill="x")

tk.Label(decision_frame, text="📢 Investment Decision", font=("Helvetica", 12, "bold"), fg=ACCENT_COLOR, bg=CARD_COLOR).pack(pady=3)
decision_label = tk.Label(decision_frame, textvariable=decision_text, font=("Helvetica", 12), fg=TEXT_COLOR, bg=CARD_COLOR, wraplength=500, justify="left")
decision_label.pack(pady=5)

# Function to analyze stock risk
def analyze_stock():
    ticker = stock_entry.get().upper().strip()
    
    if not ticker:
        messagebox.showerror("Input Error", "Please enter a valid stock ticker.")
        return
    
    try:
        data = yf.download(ticker, period="5y")
        
        if "Adj Close" in data.columns:
            prices = data["Adj Close"]
        elif "Close" in data.columns:
            prices = data["Close"]
        else:
            raise ValueError("Stock data is missing required price columns.")
        
        returns = prices.pct_change().dropna()

        # Calculate Metrics
        var_95 = returns.quantile(0.05).item()
        cvar_95 = returns[returns <= var_95].mean().item()
        std_dev = returns.std().item()
        sharpe_ratio = (returns.mean() / returns.std()).item()
        downside_returns = returns[returns < 0]
        sortino_ratio = (returns.mean() / downside_returns.std()).item()
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        max_drawdown = drawdown.min().item()

        # Update UI
        var_text.set(f"{var_95:.4f}")
        cvar_text.set(f"{cvar_95:.4f}")
        volatility_text.set(f"{std_dev:.4f}")
        sharpe_text.set(f"{sharpe_ratio:.4f}")
        sortino_text.set(f"{sortino_ratio:.4f}")
        drawdown_text.set(f"{max_drawdown:.4f}")

        # Decision-Making Analysis
        if sharpe_ratio > 1 and max_drawdown > -0.2:
            decision_text.set("✅ This stock has a good risk-adjusted return and moderate drawdown. Likely a good investment.")
        elif sharpe_ratio < 0.5 and max_drawdown < -0.4:
            decision_text.set("⚠️ High drawdown and poor risk-adjusted returns. Consider this a high-risk investment.")
        else:
            decision_text.set("⚖️ Moderate risk-return profile. Evaluate other factors before investing.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# Function to save results
def save_results():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            data = {
                "VaR (95%)": [var_text.get()],
                "CVaR (95%)": [cvar_text.get()],
                "Volatility": [volatility_text.get()],
                "Sharpe Ratio": [sharpe_text.get()],
                "Sortino Ratio": [sortino_text.get()],
                "Max Drawdown": [drawdown_text.get()],
                "Decision": [decision_text.get()]
            }
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Results saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")

# Buttons
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=20)

analyze_button = ttk.Button(button_frame, text="Analyze", command=analyze_stock, style="TButton")
analyze_button.grid(row=0, column=0, padx=10)

save_button = ttk.Button(button_frame, text="Save Results", command=save_results, style="TButton")
save_button.grid(row=0, column=1, padx=10)

# Apply Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background=ACCENT_COLOR, foreground="black")
style.map("TButton", background=[("active", "#e6b800")])

# Run App
root.mainloop()
