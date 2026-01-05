import tkinter as tkk
from tkinter import ttk
from datetime import datetime
import pandas as pd
import test_recom
import yfinance as yf
import mplfinance as mpf

def launch_recommendation_page():
    root = tkk.Toplevel()
    root.title("SmartStock Recommendations")
    root.geometry("1000x600")
    root.state('zoomed')

    # ---------- Header ----------
    tkk.Label(root, text="SmartStock: Candlestick-Based Recommendations", font=("Helvetica", 16, "bold")).pack(pady=10)

    # ---------- Button Frame ----------
    button_frame = tkk.Frame(root)
    button_frame.pack(pady=10, anchor="center")
    button_frame.columnconfigure((0, 1, 2), weight=1)

    current_filter = tkk.StringVar(value="")  # Track current filter

    def filter_action(action_type):
        current_filter.set(action_type)
        tree.delete(*tree.get_children())
        recommendations = test_recom.generate_recommendations()
        for rec in recommendations:
            if rec["Recommendation"] == action_type:
                values = (
                    rec["Ticker"],
                    rec["Daily Pattern"] or "",
                    rec["Weekly Pattern"] or "",
                    rec["Preferred Pattern"] or "",
                    rec["Timeframe"],
                    rec["Recommendation"]
                )
                tree.insert("", "end", values=values, tags=(rec["Recommendation"],))

    btn_buy = tkk.Button(button_frame, text="Buy", width=12, bg="#d4fcd4", command=lambda: filter_action("Buy"))
    btn_sell = tkk.Button(button_frame, text="Sell", width=12, bg="#fcd4d4", command=lambda: filter_action("Sell"))
    btn_watch = tkk.Button(button_frame, text="Watch", width=12, bg="#fcfcd4", command=lambda: filter_action("Watch"))

    btn_buy.pack(side="left", padx=20)
    btn_sell.pack(side="left", padx=20)
    btn_watch.pack(side="left", padx=20)

    # ---------- Treeview ----------
    style = ttk.Style()
    style.configure("Treeview", rowheight=28, font=("Helvetica", 11))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    columns = ("Ticker", "Daily Pattern", "Weekly Pattern", "Preferred Pattern", "Timeframe", "Recommendation")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

    for col in columns:
        tree.heading(col, text=col, anchor='center')
        tree.column(col, anchor='center', width=130)

    tree.tag_configure("Buy", background="#d4fcd4")
    tree.tag_configure("Sell", background="#fcd4d4")
    tree.tag_configure("Hold", background="#fcfcd4")
    tree.tag_configure("Watch", background="#fcfcd4")

    tree.pack(fill="both", expand=True)

    # ---------- Utility Buttons ----------
    utility_frame = tkk.Frame(root)
    utility_frame.pack(fill='x', pady=10)
    utility_frame.columnconfigure((0, 1, 2), weight=1)

    def refresh_data():
        tree.delete(*tree.get_children())

    tkk.Button(utility_frame, text="Clear Table", command=refresh_data).grid(row=0, column=0, padx=5, sticky='ew')

    def export_csv():
        rows = []
        for child in tree.get_children():
            values = tree.item(child)["values"]
            if any(values):  # Skip empty preview row
                rows.append({
                    "Ticker": values[0],
                    "Daily Pattern": values[1],
                    "Weekly Pattern": values[2],
                    "Preferred Pattern": values[3],
                    "Timeframe": values[4],
                    "Recommendation": values[5]
                })
        if rows:
            df = pd.DataFrame(rows)
            today = datetime.now().strftime("%Y-%m-%d")  # Format:YYYY-MM-DD
            filename = f"{current_filter.get()}recommendations{today}.csv"
            df.to_csv(filename, index=False)
            print(f"Exported to {filename}")
        else:
            print("No data to export.")

    tkk.Button(utility_frame, text="Export to CSV", command=export_csv).grid(row=0, column=1, padx=5, sticky='ew')

    def plot_candlestick(ticker, timeframe="1d", period="1mo"):
        data = yf.download(ticker, period=period, interval=timeframe, auto_adjust=True)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in data.columns for col in required_cols):
            print(f"Missing required OHLC columns for {ticker}: {data.columns}")
            return

        data = data.dropna(subset=required_cols)
        data.index.name = 'Date'
        mpf.plot(data, type='candle', style='charles', title=f"{ticker} Candlestick Chart", volume=True)

    def view_chart():
        selected = tree.focus()
        if selected:
            ticker = tree.item(selected)["values"][0]
            if not ticker.endswith(".NS"):
                ticker += ".NS"
            plot_candlestick(ticker)

    tkk.Button(utility_frame, text="View Chart", command=view_chart).grid(row=0, column=2, padx=5, sticky='ew')

    # ---------- Initial Table Preview ----------
    tree.insert("", "end", values=("", "", "", "", "", ""))

    #root.mainloop()
