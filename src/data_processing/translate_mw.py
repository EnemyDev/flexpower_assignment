from pathlib import Path
import pandas as pd

data_folder = Path(__file__).parent.absolute() / "../../data/"

def mw_to_mwh():
    from .provider import load_cleaned_data  # Moved import inside the function
    df = load_cleaned_data()
    print(df.head())
    df['Wind_DA_MWh'] = df['WindDayAheadForecastMW'] * 0.25
    df['Wind_ID_MWh'] = df['WindIntradayForecastMW'] * 0.25
    df['PV_DA_MWh'] = df['PVDayAheadForecastMW'] * 0.25
    df['PV_ID_MWh'] = df['PVIntradayForecastMW'] * 0.25
    df.to_csv(data_folder / 'processed/mwh.csv', index=False)