import pandas as pd

def find_spread_hours(df):
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    df = df.sort_values('Datetime')

    # Calculate average price differences for each hour
    hourly_price_diff = df.groupby(df['Datetime'].dt.hour).agg({
        'DayAheadPriceHourlyEURMWh': 'mean',
        'IntradayPriceHourlyEURMWh': 'mean'
    }).reset_index()
    hourly_price_diff['Price_Difference'] = hourly_price_diff['IntradayPriceHourlyEURMWh'] - hourly_price_diff['DayAheadPriceHourlyEURMWh']

    # Identify hours where, on average, intraday prices are higher than day-ahead prices
    buy_hours = hourly_price_diff[hourly_price_diff['Price_Difference'] > 0]['Datetime'].tolist()
    for buy_hour in buy_hours:
        print(f'Buy on day-ahead and sell intra-day at {buy_hour}:00')

    return buy_hours