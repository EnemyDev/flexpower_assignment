import pandas as pd

def find_best_hours(df, price_col):
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')    
    hourly_avg_prices = df.groupby(df['Datetime'].dt.hour)[price_col].mean().sort_values()
    charge_hours = hourly_avg_prices.index[:3]
    discharge_hours = hourly_avg_prices.index[-3:][::-1]
    return charge_hours, discharge_hours