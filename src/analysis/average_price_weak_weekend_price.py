import pandas as pd
from ..data_processing import provider

def weekday_vs_weekend_prices():
    df = provider.load_cleaned_data()
    # Convert 'time' to datetime for day type classification
    df['Datetime'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    
    # Classify days into weekdays and weekends
    df['DayType'] = df['Datetime'].dt.dayofweek
    df['DayType'] = df['DayType'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

    # Group by DayType and hour to get average price
    hourly_prices = df.groupby([df['Datetime'].dt.hour, 'DayType'])['DayAheadPriceHourlyEURMWh'].mean().unstack()

    # Rename columns for clarity
    hourly_prices.columns = ['Weekday', 'Weekend']
    # Calculate overall average prices
    avg_weekday_price = hourly_prices['Weekday'].mean()
    avg_weekend_price = hourly_prices['Weekend'].mean()
    return {
        "avg_weekday_price": avg_weekday_price,
        "avg_weekend_price": avg_weekend_price
    }

    print(f"\nAverage Day Ahead Price during Weekdays: {avg_weekday_price:.2f} EUR/MWh")
    print(f"Average Day Ahead Price during Weekends: {avg_weekend_price:.2f} EUR/MWh")

    # # Explanation
    # print("\nExplanation:")
    # print("- Weekday prices might be higher due to increased industrial and commercial demand.")
    # print("- Weekend prices could be lower if there's less industrial activity, although demand from residential use might increase.")
    # print("- Other factors like maintenance schedules, public holidays, or seasonal variations can also affect these averages.")
