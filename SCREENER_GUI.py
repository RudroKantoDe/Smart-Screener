import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Backend imports
import All_equity_download as update
import Download_equity_l as EQL
import Daily_doji_GUI as DD
import weekly_Doji_GUI as WD
import Daily_engulf_GUI as DE
import weekly_engulfing_GUI as WE
import Daily_insider_candle_GUI as DI
import weekly_insider_candle_GUI as WI
import Daily_Gap_GUI as DG
import Weekly_Gap_GUI as WG

def launch_screener():
    root = tk.Tk()
    root.title("🔍 SmartStock Screener")
    root.geometry("1200x750")
    root.configure(bg="#f0f2f5")
    root.state('zoomed')

    def go_back_to_dashboard():
        root.destroy()  # This closes the screener window

    # ---------------- Top Bar ----------------
    top_bar = tk.Frame(root, bg="#f0f2f5", height=60)
    top_bar.pack(side="top", fill="x")

    back_btn = tk.Button(top_bar, text="← Back", font=("Arial", 10),
                     bg="#6c757d", fg="white", padx=10, pady=5,
                     command=go_back_to_dashboard)
    back_btn.pack(side="left", padx=(10, 0), pady=10)

    tk.Label(top_bar, text="SmartStock Screener", font=("Arial", 18, "bold"),
             bg="#f0f2f5", fg="#333").pack(side="left", padx=20, pady=10)
    
    #refresh_btn = tk.Button(top_bar, text="🔁 Update EOD Data", font=("Arial", 10),
                            #bg="#28a745", fg="white", padx=10, pady=5,
                            #command=lambda: on_update_stocks())

    #refresh_btn.pack(side="right", padx=20)

    # ---------------- Main Frame ----------------
    main_frame = tk.Frame(root, bg="#f7faff")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    #-------------pattern and update frame-----------
    pattern_frame = tk.LabelFrame(main_frame, text="Candlestick Patterns",
                              font=("Arial", 12, "bold"), bg="#f7faff", padx=10, pady=10)
    pattern_frame.pack(fill="x", padx=10, pady=10)

    update_frame = tk.Frame(main_frame, bg="#f7faff")
    update_frame.pack(fill="x", padx=10, pady=(0, 20))

    # ---------------- Table Frame ----------------
    table_frame = tk.Frame(main_frame, bg="#ffffff")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Ticker", "Company", "Price", "% Change", "Pattern")
    scrollbar = tk.Scrollbar(table_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # ✅ Configuring row tags with respective colors
    tree.tag_configure("green", background="#d4f4dd")  # Light green for Green Doji
    tree.tag_configure("red", background="#fddddd")    # Light red for Red Doji


    tree.pack(fill="both", expand=True)
    

    def update_table(data, label):
        tree.delete(*tree.get_children())
        for row in data:
            pattern = row[-1]  # Last column is "Pattern"
            tag = (
                "green" if "Green" in pattern or "Bullish Engulfing" in pattern or "Gap Up" in pattern else
                "red" if "Red" in pattern or "Bearish Engulfing" in pattern or "Gap Down" in pattern else
                ""
            )
            tree.insert("", "end", values=row, tags=(tag,))
        messagebox.showinfo("Results Loaded", f"{label} screening complete.")

    btn_frame = tk.Frame(main_frame, bg="#f7faff")
    btn_frame.pack(side="left", anchor="n", padx=10)

    center_btn_frame = tk.Frame(update_frame, bg="#f7faff")
    center_btn_frame.pack(anchor="center")

    footer_frame = tk.Frame(root, bg="#e9ecef", relief="sunken", bd=1)
    footer_frame.pack(side="bottom", fill="x")

    btn_config = {"font": ("Arial", 13), "width": 25, "bg": "#007ACC", "fg": "white", "padx": 10, "pady": 8}
    btn_config1 = {"font": ("Arial", 13), "width": 25, "bg": "#28a745", "fg": "white", "padx": 10, "pady": 8}

    # ---------------- Pattern Selection Popups ----------------
    def choose_doji():
        popup = tk.Toplevel(root)
        popup.title("Choose Doji Pattern")
        popup.geometry("300x150")
        tk.Label(popup, text="Select timeframe:", font=("Arial", 12)).pack(pady=10)
    
        def run_doji_daily():
            results = DD.check_doji()
            update_table(results, "Daily Doji")
            popup.destroy()

        def run_doji_weekly():
            results = WD.check_doji()
            update_table(results, "Weekly Doji")
            popup.destroy()

        tk.Button(popup, text="Daily", command=run_doji_daily).pack(pady=5,expand=True)
        tk.Button(popup, text="Weekly", command=run_doji_weekly).pack(pady=5,expand=True)
    
    def choose_engulfing():
        popup = tk.Toplevel(root)
        popup.title("Choose Engulfing Pattern")
        popup.geometry("300x150")
        tk.Label(popup, text="Select timeframe:", font=("Arial", 12)).pack(pady=10)

        def run_engulfing_daily():
            results = DE.check_engulfing()
            update_table(results, "Daily Engulfing")
            popup.destroy()

        def run_engulfing_weekly():
            results = WE.check_engulfing()
            update_table(results, "Weekly Engulfing")
            popup.destroy()

        tk.Button(popup, text="Daily", command=run_engulfing_daily).pack(pady=5)
        tk.Button(popup, text="Weekly", command=run_engulfing_weekly).pack(pady=5)

    def choose_insider():
        popup = tk.Toplevel(root)
        popup.title("Choose Insider Candle")
        popup.geometry("300x150")
        tk.Label(popup, text="Select timeframe:", font=("Arial", 12)).pack(pady=10)

        def run_insider_daily():
            results = DI.check_insider()
            update_table(results, "Daily Insider Candle")
            popup.destroy()

        def run_insider_weekly():
            results = WI.check_insider()
            update_table(results, "Weekly Insider Candle")
            popup.destroy()

        tk.Button(popup, text="Daily", command=run_insider_daily).pack(pady=5)
        tk.Button(popup, text="Weekly", command=run_insider_weekly).pack(pady=5)
    def choose_gap_daily():
        popup = tk.Toplevel(root)
        popup.title("Daily Gap")
        popup.geometry("300x150")
        tk.Label(popup, text="Select gap type:", font=("Arial", 12)).pack(pady=10)

        def run_gap_up():
            results = DG.check_gap_up()
            update_table(results, "Daily Gap Up")
            popup.destroy()

        def run_gap_down():
            results = DG.check_gap_down()
            update_table(results, "Daily Gap Down")
            popup.destroy()

        tk.Button(popup, text="Gap Up", command=run_gap_up).pack(pady=5)
        tk.Button(popup, text="Gap Down", command=run_gap_down).pack(pady=5)

    def choose_gap_weekly():
        popup = tk.Toplevel(root)
        popup.title("Weekly Gap")
        popup.geometry("300x150")
        tk.Label(popup, text="Select gap type:", font=("Arial", 12)).pack(pady=10)

        def run_gap_up():
            results = WG.check_gap_up()
            update_table(results, "Weekly Gap Up")
            popup.destroy()

        def run_gap_down():
            results = WG.check_gap_down()
            update_table(results, "Weekly Gap Down")
            popup.destroy()

        tk.Button(popup, text="Gap Up", command=run_gap_up).pack(pady=5)
        tk.Button(popup, text="Gap Down", command=run_gap_down).pack(pady=5)
    
    def on_update_stocks():
        EQL.download_csv()
        update.datadownload()
        now = datetime.now().strftime("%d %b %Y, %I:%M %p")
        last_updated_label.config(text=f"Last updated: {now}")
        messagebox.showinfo("Update EOD", "End-Of-Day stock data updated successfully.")
    # ---------------- Buttons ----------------

    tk.Button(pattern_frame, text="📈 Doji Pattern", command=choose_doji, **btn_config).pack(side="left", padx=7,expand=True)
    tk.Button(pattern_frame, text="📊 Engulfing Pattern", command=choose_engulfing, **btn_config).pack(side="left", padx=7,expand=True)
    tk.Button(pattern_frame, text="📉 Insider Candle", command=choose_insider, **btn_config).pack(side="left", padx=7,expand=True)
    tk.Button(pattern_frame, text="📊 Daily Gap", command=choose_gap_daily, **btn_config).pack(side="left", padx=7,expand=True)
    tk.Button(pattern_frame, text="📈 Weekly Gap", command=choose_gap_weekly, **btn_config).pack(side="left", padx=7,expand=True)

    tk.Button(center_btn_frame, text="🔁 Update EOD Data", command=on_update_stocks, **btn_config1).pack()

        # Left: Last updated
    last_updated_label = tk.Label(footer_frame, text="Last updated: Not yet", anchor="w",
                                  font=("Arial", 10), bg="#e9ecef")
    last_updated_label.pack(side="left", padx=10)

        # Right: Developer tag
    dev_label = tk.Label(footer_frame, text="Developed by Rudro, 4th Year CSE",
                         anchor="e", font=("Arial", 10, "bold"),
                         bg="#000000", fg="#ffffff", padx=10, pady=2)
    dev_label.pack(side="right", padx=10)


    root.mainloop()
