import pandas as pd
from ..data_processing.provider import load_cleaned_mw_data

def get_average_product_value():
    # Calculate the average value for Wind and PV using Day Ahead prices
    df = load_cleaned_mw_data()
    
    df['Wind_Value_DA'] = df['Wind_DA_MWh'] * df['DayAheadPriceHourlyEURMWh']
    df['PV_Value_DA'] = df['PV_DA_MWh'] * df['DayAheadPriceHourlyEURMWh']

    df['Date'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M').dt.date
    
    numerical_cols = ['Wind_DA_MWh', 'Wind_ID_MWh', 'PV_DA_MWh', 'PV_ID_MWh', 'Wind_Value_DA', 'PV_Value_DA']
    daily_sums = df.groupby('Date')[numerical_cols].sum()
    
    avg_wind_value = daily_sums['Wind_Value_DA'].mean() / daily_sums['Wind_DA_MWh'].mean()
    avg_pv_value = daily_sums['PV_Value_DA'].mean() / daily_sums['PV_DA_MWh'].mean()

    avg_da_price = df['DayAheadPriceHourlyEURMWh'].mean()

    return {"Average wind value": avg_wind_value, 
              "Average PV value": avg_pv_value, 
              "Average DA price": avg_da_price} 