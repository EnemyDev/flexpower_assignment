import pandas as pd
import matplotlib.pyplot as plt
import uuid

def find_best_hours(df, price_col):
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')    
    hourly_avg_prices = df.groupby(df['Datetime'].dt.hour)[price_col].mean().sort_values()
    charge_hours = hourly_avg_prices.index[:3]
    discharge_hours = hourly_avg_prices.index[-3:][::-1] 

    return charge_hours, discharge_hours

def backtest_strategy(df, charge_hour, discharge_hour, strategy_name, price_col):
    df = df.sort_values('Datetime')
    
    daily_charge_prices = df[df['Datetime'].dt.hour == charge_hour].groupby(df['Datetime'].dt.date).first()
    daily_discharge_prices = df[df['Datetime'].dt.hour == discharge_hour].groupby(df['Datetime'].dt.date).first()
    
    daily_prices = pd.merge(daily_charge_prices, 
                            daily_discharge_prices, 
                            left_index=True, 
                            right_index=True, 
                            suffixes=('_charge', '_discharge'))
    trades = []
    for date, row in daily_prices.iterrows():
        charge_time = row['Datetime_charge'].time()
        discharge_time = row['Datetime_discharge'].time()
        
        trades.append({
            'id': str(uuid.uuid4()),
            'Datetime': pd.Timestamp.combine(date, charge_time).strftime('%m/%d/%y %H:%M'),
            'quantity': 100,  
            'price': row[f'{price_col}_charge'],
            'side': 'buy',
            'strategy': strategy_name,
            'time': str(charge_time)
        })
        trades.append({
            'id': str(uuid.uuid4()),
            'Datetime': pd.Timestamp.combine(date, discharge_time).strftime('%m/%d/%y %H:%M'),
            'quantity': 100,  
            'price': row[f'{price_col}_discharge'],
            'side': 'sell',
            'strategy': strategy_name,
            'time': str(discharge_time)
        })

    strategy_df = pd.DataFrame(trades)
    strategy_df['Revenue'] = strategy_df.apply(lambda row: (row['price'] * row['quantity'] if row['side'] == 'sell' else -row['price'] * row['quantity']), axis=1)
    strategy_df['Cumulative_Profit'] = strategy_df['Revenue'].cumsum()
    
    return strategy_df

def calculate_metrics(df):
    df['High_Water_Mark'] = df['Cumulative_Profit'].cummax()
    df['Drawdown'] = df['High_Water_Mark'] - df['Cumulative_Profit']
    max_drawdown = df['Drawdown'].max()
    df['Low_Water_Mark'] = df['Cumulative_Profit'].cummin()
    df['Runup'] = df['Cumulative_Profit'] - df['Low_Water_Mark']
    max_runup = df['Runup'].max()
    
    df['Daily_Profit_Sign'] = df.groupby(pd.to_datetime(df['Datetime'], format='%m/%d/%y %H:%M').dt.date)['Revenue'].transform(lambda x: 1 if x.sum() > 0 else (-1 if x.sum() < 0 else 0))
    df['Streak'] = (df['Daily_Profit_Sign'].shift() != df['Daily_Profit_Sign']).cumsum()
    
    win_streaks = df[df['Daily_Profit_Sign'] == 1].groupby('Streak').size()
    lose_streaks = df[df['Daily_Profit_Sign'] == -1].groupby('Streak').size()
    
    max_win_streak = win_streaks.max() if not win_streaks.empty else 0
    max_lose_streak = lose_streaks.max() if not lose_streaks.empty else 0

    total_wins = (df.groupby(pd.to_datetime(df['Datetime'], format='%m/%d/%y %H:%M').dt.date)['Revenue'].sum() > 0).sum()
    total_losses = (df.groupby(pd.to_datetime(df['Datetime'], format='%m/%d/%y %H:%M').dt.date)['Revenue'].sum() < 0).sum()

    final_profit = df['Cumulative_Profit'].iloc[-1] if not df.empty else 0

    return max_drawdown, max_runup, max_win_streak, max_lose_streak, total_wins, total_losses, final_profit

def plot_equity_curves(df, price_col):
    charge_hours, discharge_hours = find_best_hours(df, price_col)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    for ch in charge_hours:
        for dh in discharge_hours:
            strategy = backtest_strategy(df, ch, dh, f"annual_{ch}_{dh}_{price_col}", price_col)
            ax.plot(pd.to_datetime(strategy['Datetime'], format='%m/%d/%y %H:%M').dt.date, strategy['Cumulative_Profit'], 
                    label=f'{price_col} - Charge {ch}:00 - Discharge {dh}:00')
            strategy.to_csv(f'annual_{ch}_{dh}_{price_col}.csv', index=False)

    ax.set_title(f'Equity Curves for Different Battery Trading Strategies ({price_col})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Profit (EUR)')
    ax.legend()
    ax.grid(True)
    plt.show()

def find_best_quarterly_strategy(df, price_col):
    df['Quarter'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M').dt.to_period('Q')
    charge_hours, discharge_hours = find_best_hours(df, price_col)
    best_quarterly_strategies = {}
    
    for quarter, group in df.groupby('Quarter'):
        best_performance = 0
        best_pair = None
        
        for ch in charge_hours:
            for dh in discharge_hours:
                strategy = backtest_strategy(group, ch, dh, f"quarterly_{ch}_{dh}_{price_col}", price_col)
                if not strategy.empty:
                    performance = strategy['Cumulative_Profit'].iloc[-1] if len(strategy) > 0 else 0
                    if performance > best_performance:
                        best_performance = performance
                        best_pair = (ch, dh)
        
        if best_pair:
            best_quarterly_strategies[quarter] = best_pair
    
    return best_quarterly_strategies

def plot_quarterly_best_strategy(df, price_col):
    best_quarterly_strategies = find_best_quarterly_strategy(df, price_col)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    cumulative_profit = 0
    all_strategies = []

    for quarter, group in df.groupby('Quarter'):
        if quarter in best_quarterly_strategies:
            charge_hour, discharge_hour = best_quarterly_strategies[quarter]
            strategy_name = f"quarterly_{charge_hour}_{discharge_hour}_{price_col}"
            strategy = backtest_strategy(group, charge_hour, discharge_hour, strategy_name, price_col)
            if not strategy.empty:
                if all_strategies:
                    last_profit = all_strategies[-1]['Cumulative_Profit'].iloc[-1]
                    strategy['Cumulative_Profit'] += last_profit
                all_strategies.append(strategy)
            
            print(f"Quarter {quarter}: Best Strategy ({price_col}) - Charge at {charge_hour}:00, Discharge at {discharge_hour}:00")
            strategy.to_csv(f'{strategy_name}.csv', index=False)
    
    if all_strategies:
        quarterly_strategy = pd.concat(all_strategies, ignore_index=True)
        ax.plot(pd.to_datetime(quarterly_strategy['Datetime'], format='%m/%d/%y %H:%M').dt.date, quarterly_strategy['Cumulative_Profit'], 
                label=f'Best Quarterly Strategy ({price_col})', color='black', linewidth=2)
    
    ax.set_title(f'Best Quarterly Strategy Equity Curve ({price_col})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Profit (EUR)')
    ax.legend()
    ax.grid(True)
    plt.show()

df = pd.read_csv('cleaned.csv', 
                 parse_dates=['time'], 
                 date_format='%m/%d/%y %H:%M')

price_columns = ['DayAheadPriceHourlyEURMWh', 'IntradayPriceHourlyEURMWh'] 

metrics_comparison = {}

for price_col in price_columns:
    plot_equity_curves(df, price_col)

    plot_quarterly_best_strategy(df, price_col)

    charge_hours, discharge_hours = find_best_hours(df, price_col)
    best_annual_profit = 0
    best_annual_strategy = None
    for ch in charge_hours:
        for dh in discharge_hours:
            strategy = backtest_strategy(df, ch, dh, f"annual_{ch}_{dh}_{price_col}", price_col)
            metrics = calculate_metrics(strategy)
            metrics_comparison[f"{price_col}_annual_{ch}_{dh}"] = metrics
            print(f"Strategy ({price_col}): Charge {ch}:00 - Discharge {dh}:00")
            print(f"  Maximum Drawdown: {metrics[0]:.2f}")
            print(f"  Maximum Runup: {metrics[1]:.2f}")
            print(f"  Maximum Win Streak: {metrics[2]}")
            print(f"  Maximum Lose Streak: {metrics[3]}")
            print(f"  Total Wins: {metrics[4]}")
            print(f"  Total Losses: {metrics[5]}")
            print(f"  Final Cumulative Profit: {metrics[6]:.2f}\n")
            if metrics[6] > best_annual_profit:  
                best_annual_profit = metrics[6]
                best_annual_strategy = metrics

    metrics_comparison[f"best_annual_{price_col}"] = best_annual_strategy

    best_quarterly_strategies = find_best_quarterly_strategy(df, price_col)
    cumulative_profit = 0
    all_strategies = []
    for quarter, group in df.groupby('Quarter'):
        if quarter in best_quarterly_strategies:
            charge_hour, discharge_hour = best_quarterly_strategies[quarter]
            strategy_name = f"quarterly_{charge_hour}_{discharge_hour}_{price_col}"
            strategy = backtest_strategy(group, charge_hour, discharge_hour, strategy_name, price_col)
            if not strategy.empty:
                if all_strategies:
                    last_profit = all_strategies[-1]['Cumulative_Profit'].iloc[-1]
                    strategy['Cumulative_Profit'] += last_profit
                all_strategies.append(strategy)

    if all_strategies:
        quarterly_strategy = pd.concat(all_strategies, ignore_index=True)
        quarterly_metrics = calculate_metrics(quarterly_strategy)
        metrics_comparison[f"best_quarterly_{price_col}"] = quarterly_metrics
        print(f"Best Quarterly Strategy Metrics ({price_col}):")
        print(f"  Maximum Drawdown: {quarterly_metrics[0]:.2f}")
        print(f"  Maximum Runup: {quarterly_metrics[1]:.2f}")
        print(f"  Maximum Win Streak: {quarterly_metrics[2]}")
        print(f"  Maximum Lose Streak: {quarterly_metrics[3]}")
        print(f"  Total Wins: {quarterly_metrics[4]}")
        print(f"  Total Losses: {quarterly_metrics[5]}")
        print(f"  Final Cumulative Profit: {quarterly_metrics[6]:.2f}\n")

print("\nComparison of DA vs ID Prices:")
for strategy_type in ['best_annual', 'best_quarterly']:
    da_profit = metrics_comparison[f"{strategy_type}_DayAheadPriceHourlyEURMWh"][6] if f"{strategy_type}_DayAheadPriceHourlyEURMWh" in metrics_comparison else 0
    id_profit = metrics_comparison[f"{strategy_type}_IntradayPriceHourlyEURMWh"][6] if f"{strategy_type}_IntradayPriceHourlyEURMWh" in metrics_comparison else 0
    
    profit_diff = id_profit - da_profit
    better_market = "Intraday" if profit_diff > 0 else "Day-Ahead" if profit_diff < 0 else "Equal"
    print(f"{strategy_type.capitalize()} Strategy:")
    print(f"  Profit Difference (ID - DA): {profit_diff:.2f}")
    print(f"  Better Market: {better_market}")
    print()