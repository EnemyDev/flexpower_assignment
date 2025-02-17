from pathlib import Path
from ..data_processing.provider import load_cleaned_mw_data

data_folder = (Path(__file__).parent.absolute() / "../../../data/").resolve()

def get_forecast_sum():
    df = load_cleaned_mw_data()
    totals = df.sum()
    return {"Wind DA MWh for 2021": totals['Wind_DA_MWh'],
            "Wind ID MWh for 2021": totals['Wind_ID_MWh'],
            "PV DA MWh for 2021": totals['PV_DA_MWh'],
            "PV ID MWh for 2021": totals['PV_ID_MWh']}