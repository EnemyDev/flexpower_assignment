import pandas as pd
import matplotlib.pyplot as plt
from ...analysis.best_hours import find_best_hours
from .battery_backtest import backtest_and_cache

def find_best_quarterly_strategy(df, price_col, strategy_cache):
    df['Quarter'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M').dt.to_period('Q')
    charge_hours, discharge_hours = find_best_hours(df, price_col)
    best_quarterly_strategies = {}
    
    for quarter, group in df.groupby('Quarter'):
        best_performance = float('-inf')
        best_pair = None
        
        for ch in charge_hours:
            for dh in discharge_hours:
                strategy_name = f"quarterly_{ch}_{dh}_{price_col}_{quarter}"
                strategy = backtest_and_cache(group, ch, dh, strategy_name, price_col, strategy_cache)
                performance = strategy['Cumulative_Profit'].iloc[-1] if not strategy.empty else float('-inf')
                if performance > best_performance:
                    best_performance = performance
                    best_pair = (ch, dh)
        
        if best_pair:
            best_quarterly_strategies[quarter] = best_pair
    
    return best_quarterly_strategies