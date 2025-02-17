import uuid
import pandas as pd

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
            'quantity': 100,  # Represents 100 MWh
            'price': row[f'{price_col}_charge'],
            'side': 'buy',
            'strategy': strategy_name,
            'time': str(charge_time)
        })
        trades.append({
            'id': str(uuid.uuid4()),
            'Datetime': pd.Timestamp.combine(date, discharge_time).strftime('%m/%d/%y %H:%M'),
            'quantity': 100,  # Represents 100 MWh
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

def backtest_and_cache(df, charge_hour, discharge_hour, strategy_name, price_col, strategy_cache):
    key = (charge_hour, discharge_hour, price_col)
    if key not in strategy_cache:
        strategy_cache[key] = backtest_strategy(df, charge_hour, discharge_hour, strategy_name, price_col)
    return strategy_cache[key]