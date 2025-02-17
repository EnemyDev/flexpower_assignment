import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from .battery_strategy import find_best_quarterly_strategy
from .battery_backtest import backtest_and_cache
from ...analysis.best_hours import find_best_hours

data_folder = (Path(__file__).parent.absolute() / "../../../data/").resolve()

def plot_equity_curves(df, price_col, strategy_cache):
    str_path = str(data_folder / "processed" / "trades" / "battery")
    os.makedirs(str_path, exist_ok=True)
    charge_hours, discharge_hours = find_best_hours(df, price_col)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    for ch in charge_hours:
        for dh in discharge_hours:
            strategy_name = f"annual_{ch}_{dh}_{price_col}"
            strategy = backtest_and_cache(df, ch, dh, strategy_name, price_col, strategy_cache)
            ax.plot(pd.to_datetime(strategy['Datetime'], format='%m/%d/%y %H:%M').dt.date, strategy['Cumulative_Profit'], 
                    label=f'{price_col} - Charge {ch}:00 - Discharge {dh}:00')
            strategy.to_csv(f'{str_path}/{strategy_name}.csv', index=False)

    ax.set_title(f'Equity Curves for Different Battery Trading Strategies ({price_col})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Profit (EUR)')
    ax.legend()
    ax.grid(True)
    str_path = str(data_folder / "processed" / "charts" / "battery")
    os.makedirs(str_path, exist_ok=True)
    plt.savefig(f'{str_path}/9_best_times_{price_col}_eq.png')
    plt.show()
    

def plot_quarterly_best_strategy(df, price_col, strategy_cache):
    str_path = str(data_folder / "processed" / "trades" / "battery")
    os.makedirs(str_path, exist_ok=True)
    best_quarterly_strategies = find_best_quarterly_strategy(df, price_col, strategy_cache)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    all_strategies = []

    for quarter, group in df.groupby('Quarter'):
        if quarter in best_quarterly_strategies:
            charge_hour, discharge_hour = best_quarterly_strategies[quarter]
            strategy_name = f"quarterly_{charge_hour}_{discharge_hour}_{price_col}_{quarter}"
            strategy = backtest_and_cache(group, charge_hour, discharge_hour, strategy_name, price_col, strategy_cache)
            if not strategy.empty:
                if all_strategies:
                    last_profit = all_strategies[-1]['Cumulative_Profit'].iloc[-1]
                    strategy['Cumulative_Profit'] += last_profit
                all_strategies.append(strategy)
            
            print(f"Quarter {quarter}: Best Strategy ({price_col}) - Charge at {charge_hour}:00, Discharge at {discharge_hour}:00")
            strategy.to_csv(f'{str_path}/{strategy_name}.csv', index=False)
    
    if all_strategies:
        quarterly_strategy = pd.concat(all_strategies, ignore_index=True)
        # Plot only the equity curve, starting from the first non-zero profit
        non_zero_index = quarterly_strategy['Cumulative_Profit'].ne(0).idxmax()
        if non_zero_index is not None:
            plot_data = quarterly_strategy.loc[non_zero_index:]
            ax.plot(pd.to_datetime(plot_data['Datetime'], format='%m/%d/%y %H:%M').dt.date, plot_data['Cumulative_Profit'], 
                    label=f'Best Quarterly Strategy ({price_col})', color='black', linewidth=2)
    
    ax.set_title(f'Best Quarterly Strategy Equity Curve ({price_col})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Profit (EUR)')
    ax.legend()
    ax.grid(True)
    str_path = str(data_folder / "processed" / "charts" / "battery")
    os.makedirs(str_path, exist_ok=True)
    plt.savefig(f'{str_path}/best_quarterly_{price_col}_eq.png')
    plt.show()
    