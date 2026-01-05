import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import PRICE_UP_GUI
import PRICE_DOWN_GUI

# Hardcoded Nifty 50 tickers
nifty_50 = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
    "LT.NS", "AXISBANK.NS", "KOTAKBANK.NS", "ITC.NS", "BHARTIARTL.NS", "MARUTI.NS",
    "HINDUNILVR.NS", "ASIANPAINT.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "WIPRO.NS",
    "TECHM.NS", "POWERGRID.NS", "NTPC.NS", "COALINDIA.NS", "ONGC.NS", "CIPLA.NS",
    "DIVISLAB.NS", "TITAN.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "HCLTECH.NS",
    "ADANIENT.NS", "ADANIPORTS.NS", "BPCL.NS", "HEROMOTOCO.NS", "EICHERMOT.NS",
    "GRASIM.NS", "JSWSTEEL.NS", "DRREDDY.NS", "BRITANNIA.NS", "SBILIFE.NS",
    "HDFCLIFE.NS", "SHREECEM.NS", "NESTLEIND.NS", "M&M.NS", "TATAMOTORS.NS",
    "TATASTEEL.NS", "INDUSINDBK.NS", "BAJAJ-AUTO.NS", "HINDALCO.NS", "APOLLOHOSP.NS",
    "ICICIPRULI.NS", "LTIM.NS"
]
nifty_50_1 = [t.replace(".NS", "") for t in nifty_50]
# Fetch and sort movers
def launch_overview():
        
    # GUI setup
    root = tk.Tk()
    root.title("📊 Nifty 50 Gainers & Losers")
    root.geometry("600x400")
    root.configure(bg="#f7faff")
    root.state('zoomed')

    # Frame to hold Treeview and Scrollbar
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Treeview with scrollbar
    tree = ttk.Treeview(table_frame, columns=("Ticker", "Price", "Volume", "% Change", "Pattern"), show="headings", height=12, yscrollcommand=scrollbar.set)
    for col in ("Ticker", "Price", "Volume", "% Change", "Pattern"):
        tree.heading(col, text=col)
        if col == "Ticker":
            tree.column(col, anchor="w")  # Left-align Ticker
        else:
            tree.column(col, anchor="center")
    tree.pack(side="left", fill="both", expand=True)

    # Link scrollbar to Treeview
    scrollbar.config(command=tree.yview)

    # Row coloring
    tree.tag_configure("green", background="#e6ffe6")
    tree.tag_configure("red", background="#ffe6e6")

    #Mover function to get losers and gainers
    def get_nifty_movers(direction="gainers"):
        movers = []
        for symbol in nifty_50:
            try:
                data = yf.Ticker(symbol).history(period="2d")
                if len(data) >= 2:
                    prev_close = data.iloc[-2]['Close']
                    curr_close = data.iloc[-1]['Close']
                    volume = int(data.iloc[-1]['Volume'])
                    change = ((curr_close - prev_close) / prev_close) * 100
                    movers.append((symbol, f"{curr_close:.2f}", f"{volume}",f"{change:+.2f}%"))
            except Exception as e:
                print(f"{symbol} → {e}")

        movers.sort(key=lambda x: float(x[3].replace('%','')), reverse=True)
        if direction == "gainers":
            return [m for m in movers if "+" in m[3]]
        else:
            return [m for m in movers if "-" in m[3]]
        
    # Update gainer losers table

    def update_gainers_losers_table(data, label):
        tree.delete(*tree.get_children())
        for symbol, price, volume, change in data:        
            pattern = "🚀 Gainer" if "+" in change else "📉 Loser"
            tag = "green" if "+" in change else "red"
            clean_symbol = symbol.replace(".NS", "")
            clean_symbol=clean_symbol.strip()
            clean_symbol = clean_symbol.ljust(20)
            price=price.rjust(12)
            volume=volume.rjust(12)
            tree.insert("", "end", values=(clean_symbol, price, volume, change, pattern), tags=(tag,))
        messagebox.showinfo("Results Loaded", f"{label} loaded successfully.")

    # Update Volume shocker table

    def update_volume_shocker_table(data, label):
        tree.delete(*tree.get_children())
        for symbol, price, volume, change in data:
            pattern="Volume Shockers – Price Up" if "+" in change else "Volume Shockers – Price Down"
            tag = "green" if "+" in change else "red"
            clean_symbol = symbol.replace(".NS", "")
            clean_symbol = clean_symbol.strip()
            clean_symbol = clean_symbol.ljust(20)
            price=price.rjust(12)
            volume=volume.rjust(12)
            #print(type(clean_symbol))
            tree.insert("", "end", values=(clean_symbol, price, volume, change, pattern), tags=(tag,))
        messagebox.showinfo("Results Loaded", f"{label} loaded successfully.")
        
    # Button actions---->

    def show_gainers():
        raw_data = get_nifty_movers("gainers")
        data = [(symbol, price, volume, change) for symbol, price, volume, change in raw_data]
        update_gainers_losers_table(data, "Top Nifty Gainers")

    def show_losers():
        raw_data = get_nifty_movers("losers")
        data = [(symbol, price, volume, change) for symbol, price, volume, change in raw_data]
        update_gainers_losers_table(data, "Top Nifty Losers")

    def open_volume_shocker_popup():
        popup = tk.Toplevel(root)
        popup.title("📊 Volume Shockers")
        popup.geometry("400x200")
        popup.configure(bg="#f7faff")

        tk.Label(popup, text="Choose Volume Shocker Type", font=("Arial", 14, "bold"), bg="#f7faff").pack(pady=20)

        btn_frame = tk.Frame(popup, bg="#f7faff")
        btn_frame.pack(pady=10)

        def show_price_up_shockers():
            popup.destroy()
            data = PRICE_UP_GUI.Volumeup_priceup()
            update_volume_shocker_table(data, "Volume Shockers – Price Up")

        def show_price_down_shockers():
            popup.destroy()
            data = PRICE_DOWN_GUI.Volumeup_pricedown()
            update_volume_shocker_table(data, "Volume Shockers – Price Down")

        tk.Button(btn_frame, text="📈 Price Up Shockers", command=show_price_up_shockers,
                  font=("Arial", 11), bg="#d1f7d1", width=20).pack(side="left", padx=10)

        tk.Button(btn_frame, text="📉 Price Down Shockers", command=show_price_down_shockers,
                  font=("Arial", 11), bg="#f7d1d1", width=20).pack(side="left", padx=10)

    # Buttons
    btn_frame = tk.Frame(root, bg="#f7faff")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="📈 Show Gainers", command=show_gainers, font=("Arial", 11), bg="#d1f7d1").pack(side="left", padx=10)
    tk.Button(btn_frame, text="📉 Show Losers", command=show_losers, font=("Arial", 11), bg="#f7d1d1").pack(side="left", padx=10)
    tk.Button(btn_frame, text="📊 Volume Shockers", command=open_volume_shocker_popup, font=("Arial", 11), bg="#d1e0ff").pack(side="left", padx=10)
    root.mainloop()
