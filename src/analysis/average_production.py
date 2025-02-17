import pandas as pd
from .visualisations import chart_generator

def get_average_production_charts(mode='display'):
    from ..data_processing.provider import load_cleaned_data  # Moved import inside the function
    df = load_cleaned_data()
    hourly_avg = df.groupby('hour').agg({
        'WindDayAheadForecastMW': 'mean',
        'WindIntradayForecastMW': 'mean',
        'PVDayAheadForecastMW': 'mean',
        'PVIntradayForecastMW': 'mean'
    }).reset_index()
    chart_generator.generate_average_production_chart(hourly_avg, 
                                                      'hour', 
                                                      'Hour of Day', 
                                                      'Average Wind and Solar Production by Hour in 2021', 
                                                      'forecast_averages.png', 
                                                      major_ticks=range(24), 
                                                      grid_style='major', 
                                                      mode=mode)
    df['time'] = pd.to_datetime(df['time'], format='%m/%d/%y %H:%M')
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute

    # Create bins for 15-minute intervals
    df['minute_bin'] = df['minute']

    # Group by hour and minute_bin
    quarter_hourly_avg = df.groupby(['hour', 'minute_bin']).agg({
        'WindDayAheadForecastMW': 'mean',
        'WindIntradayForecastMW': 'mean',
        'PVDayAheadForecastMW': 'mean',
        'PVIntradayForecastMW': 'mean'
    }).reset_index()

    # Rename 'minute_bin' to 'minute' for clarity
    quarter_hourly_avg = quarter_hourly_avg.rename(columns={'minute_bin': 'minute'})

    # Combine hour and minute for plotting
    quarter_hourly_avg['time'] = quarter_hourly_avg['hour'] + quarter_hourly_avg['minute'] / 60.0

    # Generate 15-minute chart
    chart_generator.generate_average_production_chart(quarter_hourly_avg, 
                                                      'time', 
                                                      'Time of Day', 
                                                      'Average Wind and Solar Production by 15-Minute Interval in 2021', 
                                                      'forecast_averages_15min.png', 
                                                      major_ticks=range(24), 
                                                      minor_ticks=[i + j/4 for i in range(24) for j in range(4)], 
                                                      xlim=(0, 23.75), 
                                                      grid_style='both',
                                                      mode=mode)
