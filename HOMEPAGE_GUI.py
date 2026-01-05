import tkinter as tk
from tkinter import ttk
import pandas as pd
import time
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import LOGIN_GUI# Replace with your actual sign-in module name
import session
import SCREENER_GUI
import OVERVIEW_GUI
import RECOMMENDATION_GUI
import SETTINGS_GUI

current_index = 0 
tickers = ["ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
               "BPCL.NS","BHARTIARTL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS",
               "HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","INDUSINDBK.NS","INFY.NS","ITC.NS","JSWSTEEL.NS","KOTAKBANK.NS",
               "LT.NS","M&M.NS","MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS","SUNPHARMA.NS","TATACONSUM.NS",
               "TATAMOTORS.NS","TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"]
tickers1 = [t.replace(".NS", "") for t in tickers]

     # ✅ Global variable, defined before update_chart() is ever called
def launch_homepage(): 
    # ---------- Load CSV ----------
    df = pd.read_csv("EQUITY_L.csv", header=None)
    df.columns = ["Ticker", "Company", "Series", "ListingDate", "FaceValue", "MarketLot", "ISIN", "PaidUpValue"]

    # ---------- Root Window ----------
    root = tk.Tk()
    root.title("📈 SmartStock Screener (EOD + Live)")
    root.geometry("1200x750")
    root.configure(bg="#f0f2f5")
    root.state('zoomed')

    # ---------- Style ----------
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#1f2937", foreground="white")
    style.map("Treeview", background=[("selected", "#d1e7dd")])

    # ---------- Header ----------
    header = tk.Frame(root, bg="#1f2937", height=60)
    header.pack(fill="x")

    title = tk.Label(header, text="SmartStock Screener", font=("Helvetica", 18, "bold"), fg="white", bg="#1f2937")
    title.pack(side="left", padx=20)

    time_label = tk.Label(header, font=("Helvetica", 12), fg="white", bg="#1f2937")
    time_label.pack(side="right", padx=20)

    def update_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        time_label.config(text=f"📅 {current_time}")
        root.after(1000, update_time)

    update_time()
    # ---------- Rotating Ticker Marquee ----------
    ticker_canvas = tk.Canvas(root, height=30, bg="#1f2937", highlightthickness=0)
    ticker_canvas.pack(fill="x")
    ticker_text_id = None
    scroll_x = 0
    ticker_string = ""
    # ---------- Sidebar Navigation ----------

    def open_login():
        LOGIN_GUI.launch_signin(nav_buttons)    
        
    sidebar = tk.Frame(root, bg="#374151", width=180)
    sidebar.pack(side="left", fill="y")

    def on_enter(e): e.widget['background'] = '#4b5563'
    def on_leave(e): e.widget['background'] = '#374151'

    # Simulate login state (replace with actual logic later)
    # Set to False to test access control
    #is_logged_in=False
    

    # Define navigation items and their actions
    nav_items = [
        ("📊 Dashboard", lambda: print("Dashboard opened")),
        ("🔍 Screener", SCREENER_GUI.launch_screener),
        ("📈 Market Overview", OVERVIEW_GUI.launch_overview),
        ("🧠 Recommendations", RECOMMENDATION_GUI.launch_recommendation_page),
        ("⚙ Settings", SETTINGS_GUI.launch_settings)
    ]

    nav_buttons = {}

    for label, command in nav_items:
        btn = tk.Button(sidebar, text=label, font=("Helvetica", 12), fg="white", bg="#374151", bd=0)
        btn.pack(fill="x", pady=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        btn.config(command=command)

        if not session.is_logged_in and label != "📊 Dashboard":
            btn.config(state="disabled")  # Disable if not logged in
        
        nav_buttons[label] = btn #Storing the reference 
            
    login_btn = tk.Button(sidebar, text="🔐 Login", font=("Helvetica", 12), fg="white", bg="#374151", bd=0, command=open_login)
    login_btn.pack(fill="x", pady=(20, 5))  # Adds 20px space above, 5px below
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    # ---------- Main Content ----------
    main = tk.Frame(root, bg="#f0f2f5")
    main.pack(side="top", fill="both", expand=True, padx=10, pady=10)
   
    # ---------- Rotating Price -------
    ticker_frame = tk.Frame(root, bg="#1f2937", height=30)
    ticker_frame.pack(fill="x")

    ticker_text = tk.StringVar()
    ticker_label = tk.Label(ticker_frame, textvariable=ticker_text, font=("Segoe UI", 10), fg="white", bg="#1f2937")
    ticker_label.pack(side="left", padx=10)
    # ---------- Filter Button ----------
   
    # ---------- Separator ----------
    separator = ttk.Separator(main, orient='horizontal')
    separator.pack(fill='x', pady=10)

    # ---------- Market Breadth Summary ----------
    breadth_label = tk.Label(main, text="📈 Advancers: 0 | 📉 Decliners: 0", font=("Helvetica", 12), bg="#f0f2f5")
    breadth_label.pack(pady=5)

    # ---------- Live Table of Most Active Stocks ----------
    table_frame = tk.Frame(main)
    table_frame.pack(fill="both", expand=True)

    columns = ["Ticker", "Company", "Price", "% Change", "Volume"]
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # ---------- Live Data Fetching ----------
    def get_live_data(tickers):
        data = []
        advancers = 0
        decliners = 0
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                price = info.get("regularMarketPrice", 0)
                change = info.get("regularMarketChangePercent", 0)
                volume = info.get("volume", 0)
                name = info.get("shortName", ticker)
                data.append([ticker, name, price, f"{change:.2f}%", volume])
                if change > 0:
                    advancers += 1
                elif change < 0:
                    decliners += 1
            except:
                continue
        return data, advancers, decliners
    ticker_index = 0

    def fetch_ticker_string():
        messages = []
        for ticker in tickers[:50]:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                price = info.get("regularMarketPrice", "N/A")
                change = info.get("regularMarketChangePercent", 0)
                name = info.get("shortName", ticker.replace(".NS", ""))
                messages.append(f"{name}: ₹{price} ({change:+.2f}%)")
            except:
                continue
        return "   |   ".join(messages)

    scroll_x = 0
    ticker_string = ""

    def start_ticker():
        global ticker_string, scroll_x
        ticker_string = fetch_ticker_string()
        scroll_x = ticker_canvas.winfo_width()
        animate_ticker()
        

    def animate_ticker():
        global scroll_x, ticker_string, ticker_text_id
        ticker_canvas.delete("ticker")  # Remove previous text by tag
        ticker_text_id = ticker_canvas.create_text(scroll_x, 15, text=ticker_string, anchor="w", font=("Segoe UI", 10), fill="white", tags="ticker")
        scroll_x -= 2
        if scroll_x < -len(ticker_string) * 7:  # Estimate when text is off-screen
            scroll_x = ticker_canvas.winfo_width()  # Reset to right edge
        ticker_canvas.after(50, animate_ticker)

    def refresh_table():
        tree.delete(*tree.get_children())
        live_data, advancers, decliners = get_live_data(tickers[:20])
        for row in live_data:
            tree.insert("", "end", values=row)
        breadth_label.config(text=f"📈 Advancers: {advancers} | 📉 Decliners: {decliners}")
        root.after(30000, refresh_table)  # Refresh every 30 seconds

    refresh_table()
    # ---------- Separator ----------
    separator2 = ttk.Separator(main, orient='horizontal')
    separator2.pack(fill='x', pady=10)

    # ---------- Live Chart Section ----------
    chart_frame = tk.LabelFrame(main, text="📈 Live Stock Chart (Yahoo Finance)", font=("Helvetica", 14, "bold"), bg="#f0f2f5")
    chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    fig, ax = plt.subplots(figsize=(15, 3), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.get_tk_widget().pack()
     

    

    def fetch_stock_data(ticker):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d", interval="1m")
            if hist.empty:
                return pd.DataFrame()
            # Use the most recent non-empty day
            last_day = hist.index[-1].date()
            filtered = hist[hist.index.date == last_day]
            return filtered
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return pd.DataFrame()


        
    def update_chart():
        global current_index
        ticker = tickers[current_index]
        tt = tickers1[current_index]
        #print(f"Updating chart for: {ticker}")
        data = fetch_stock_data(ticker)

        ax.clear()
        if not data.empty:
            times = data.index.strftime('%H:%M')
            prices = data["Close"]

            ax.plot(times, prices, label=ticker, color="blue")
            ax.set_title(f"Live Price: {tt}", fontsize=12)
            ax.set_xlabel("Time", fontsize=10)
            ax.set_ylabel("Price", fontsize=10)
            ax.tick_params(axis='x', labelrotation=45)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_xticks(times[::max(1, len(times)//10)])

            fig.tight_layout()
        else:
            ax.text(0.5, 0.5, f"No data for {ticker}", ha='center', va='center')

        canvas.draw()
        current_index = (current_index + 1) % len(tickers)
        root.after(5000, update_chart)

    update_chart()



    # ---------- Footer ----------
    footer = tk.Frame(root, bg="#1f2937", height=20)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)
    
    credit = tk.Label(footer, text="Developed by Rudro | Final Year CSE", font=("Helvetica", 8), fg="white", bg="#1f2937")
    credit.pack(side="right", padx=10)
    
    #version = tk.Label(footer, text="v1.2", font=("Helvetica", 10), fg="white", bg="#1f2937")
    #version.pack(side="right", padx=10)

    # ---------- Run App ----------

    start_ticker()
    root.mainloop()
