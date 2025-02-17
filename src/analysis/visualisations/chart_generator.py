import matplotlib.pyplot as plt
from pathlib import Path
import os

data_folder = (Path(__file__).parent.absolute() / "../../../data/").resolve()

def generate_average_production_chart(df, time_column, xlabel, title, filename, major_ticks=None, minor_ticks=None, xlim=None, grid_style='major', mode='display'):
    plt.figure(figsize=(12, 6))
    
    for column in ['WindDayAheadForecastMW', 'WindIntradayForecastMW', 'PVDayAheadForecastMW', 'PVIntradayForecastMW']:
        label = column.split('Forecast')[0] + (' DA' if 'DayAhead' in column else ' ID')
        plt.plot(df[time_column], df[column], label=label)
    
    plt.xlabel(xlabel)
    plt.ylabel('Average Forecast (MW)')
    plt.title(title)
    plt.legend()
    
    # Setting ticks and grid based on input parameters
    if major_ticks:
        plt.xticks(major_ticks)
    if minor_ticks:
        plt.xticks(minor_ticks, minor=True)
    if xlim:
        plt.xlim(xlim)
    
    plt.grid(True, which=grid_style, linestyle='-', alpha=0.2 if grid_style == 'both' else 1)
    
    if mode == 'display':
        plt.show()
    else:
        str_path = str(data_folder / "processed" / "charts" / "average_productions")
        os.makedirs(str_path, exist_ok=True)
        plt.savefig(f'{str_path}/{filename}')
        print(f'{title} Chart saved to {str_path}/{filename}')
    