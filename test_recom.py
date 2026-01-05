import pandas as pd
from collections import defaultdict
import Daily_doji_GUI as DD
import weekly_Doji_GUI as WD
import Daily_engulf_GUI as DE
import weekly_engulfing_GUI as WE
import Daily_insider_candle_GUI as DI
import weekly_insider_candle_GUI as WI
import Daily_Gap_GUI as DG
import Weekly_Gap_GUI as WG

def generate_recommendations():

    # Daily
    doji_daily = DD.check_doji()
    #print(doji_daily)
    engulfing_daily = DE.check_engulfing() 
    insider_daily = DI.check_insider()
    gap_up_daily = DG.check_gap_up()
    gap_down_daily = DG.check_gap_down()

    # Weekly
    doji_weekly = WD.check_doji()
    engulfing_weekly = WE.check_engulfing()
    insider_weekly = WI.check_insider()
    gap_up_weekly = WG.check_gap_up()
    gap_down_weekly = WG.check_gap_down()

    stock_patterns = defaultdict(lambda: {"Daily": None, "Weekly": None})

    for name, company, close, change, pattern in doji_daily:
        stock_patterns[name]["Daily"] = pattern
    for name, company, close, change, pattern in engulfing_daily:
        stock_patterns[name]["Daily"] = pattern
    for name, company, close, change, pattern in insider_daily:
        stock_patterns[name]["Daily"] = pattern
    for name, company, close, change, pattern in gap_up_daily:
        stock_patterns[name]["Daily"] = pattern
    for name, company, close, change, pattern in gap_down_daily:
        stock_patterns[name]["Daily"] = pattern

    for name, company, close, change, pattern in doji_weekly:
        stock_patterns[name]["Weekly"] = pattern
    for name, company, close, change, pattern in engulfing_weekly:
        stock_patterns[name]["Weekly"] = pattern
    for name, company, close, change, pattern in insider_weekly:
        stock_patterns[name]["Weekly"] = pattern
    for name, company, close, change, pattern in gap_up_weekly:
        stock_patterns[name]["Weekly"] = pattern
    for name, company, close, change, pattern in gap_down_weekly:
        stock_patterns[name]["Weekly"] = pattern
    


    #Building pattern strengths

    pattern_strength = {
        "Bullish Engulfing": 3,
        "Bearish Engulfing": 3,
        "Doji": 1,
        "Insider Candle": 1,
        "Gap Up":2,
        "Gap Down":2
    }

    #Choosing the preferred pattern 
    def choose_preffered_pattern(daily,weekly):
        if weekly and (not daily or pattern_strength.get(weekly, 0) >= pattern_strength.get(daily, 0)):
            return weekly, "Weekly"
        elif daily:
            return daily, "Daily"
        else:
            return None, None

    #Mapping patterns to respective actions
        
    def recommend_action(pattern):
        if pattern in ["Bullish Engulfing","Gap Up"]:
            return "Buy"
        elif pattern in ["Bearish Engulfing","Gap Down"]:
            return "Sell"
        else:
            return "Watch"
    #Final recommendation list
    recommendations = []

    for ticker, tf_data in stock_patterns.items():
        daily = tf_data["Daily"]
        weekly = tf_data["Weekly"]
        preferred_pattern, timeframe = choose_preffered_pattern(daily,weekly)
        action = recommend_action(preferred_pattern)

        recommendations.append({
            "Ticker": ticker,
            "Daily Pattern": daily,
            "Weekly Pattern": weekly,
            "Preferred Pattern": preferred_pattern,
            "Timeframe": timeframe,
            "Recommendation": action
        })
    return recommendations
    '''
    print("HI")
    for rec in recommendations:
        print(rec)
    
    # Convert to DataFrame(Optional)
    recommend_df = pd.DataFrame(recommendations)

    recommend_df.to_csv("candlestick_recommendations.csv", index=False)
    print(recommend_df)
    '''
#generate_recommendations()
        
