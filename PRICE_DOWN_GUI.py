import pandas as pd
import os
def Volumeup_pricedown():
            results = []
            try:
                equity_details = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\GUI\\EQUITY_L.CSV')
                for name in equity_details.SYMBOL:
                    try:
                        path = f'C:\\Users\\HP\\OneDrive\\Desktop\\GUI\\DATA\\{name}.CSV'
                        if not os.path.exists(path):
                            continue

                        stock_details = pd.read_csv(path)
                        data = stock_details.tail(6)

                        vol = list(map(int, data.Volume))
                        price = list(map(float, data.Close))

                        avg_vol = sum(vol[:5]) / 5
                        vol_threshold = avg_vol * 1.2
                        price_threshold = price[-2] * 0.985
                        change = ((price[-1] - price[-2]) / price[-2]) * 100

                        if price[-1] > 100 and vol[-1] > 150000 and vol[-1] > vol_threshold and price[-1] < price_threshold:
                            results.append((name, f"{price[-1]:.2f}", f"{vol[-1]:,}", f"{change:+.2f}%"))

                    except Exception as e:
                        print(f"{name} → {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load equity list: {e}")
            return results
