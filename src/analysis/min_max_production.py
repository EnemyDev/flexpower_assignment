import pandas as pd
from ..data_processing import provider

def find_min_max_production():
    df = provider.load_cleaned_data()
    # Convert MW to MWh for quarter-hourly data
    df['Total Renewable MWh'] = (df['WindDayAheadForecastMW'] + df['PVDayAheadForecastMW']) * 0.25
    
    # Extract date from 'time'
    df['Date'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M').dt.date

    # Group by date to find daily totals and then identify high and low production days
    daily_totals = df.groupby('Date').agg({
        'Total Renewable MWh': 'sum',
        'DayAheadPriceHourlyEURMWh': 'mean'
    }).reset_index()

    # Find the day with the highest renewable energy production
    max_production_day = daily_totals.loc[daily_totals['Total Renewable MWh'].idxmax()]
    
    # Find the day with the lowest renewable energy production
    min_production_day = daily_totals.loc[daily_totals['Total Renewable MWh'].idxmin()]
    
    return {
        "max":{
            "Date": max_production_day['Date'],
            "TotalRenewableMWh": max_production_day['Total Renewable MWh'],
            "DayAheadPriceHourlyEURMWh": max_production_day['DayAheadPriceHourlyEURMWh']
            }, 
        "min":{
            "Date": min_production_day['Date'],
            "TotalRenewableMWh": min_production_day['Total Renewable MWh'],
            "DayAheadPriceHourlyEURMWh": min_production_day['DayAheadPriceHourlyEURMWh']
            }
        }


