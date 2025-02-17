from pathlib import Path
import pandas as pd
from .clean_csv import clean_csv

data_folder = (Path(__file__).parent.absolute() / "../../data/").resolve()

def load_cleaned_data() -> pd.DataFrame:
    if not (data_folder / 'processed/cleaned.csv').is_file():
        print("Cleaned file not found, cleaning csv")
        clean_csv()
        
    df = pd.read_csv(data_folder / 'processed/cleaned.csv',decimal='.')
    return df

def load_cleaned_mw_data() -> pd.DataFrame:
    from .translate_mw import mw_to_mwh  # avoid circular import error
    if not (data_folder / 'processed/mwh.csv').is_file():
        print("MWH translated file not found, generating it.")
        mw_to_mwh()
        
    df = pd.read_csv(data_folder / 'processed/mwh.csv',decimal='.',date_format='%m/%d/%y %H:%M')
    return df