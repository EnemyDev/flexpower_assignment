import sqlite3
from pathlib import Path

database_file = Path(__file__).parent.absolute() / "../../data/raw/trades.sqlite"


def compute_total_buy_volume(*args, **kwargs) -> float:
    return volume_sum('buy')

def compute_total_sell_volume(*args, **kwargs) -> float:
    return volume_sum('sell')

def volume_sum(direction: str = 'buy') -> float:
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    result = cursor.execute("SELECT SUM(quantity) FROM epex_12_20_12_13 WHERE side = " + 
                            ("'buy'" if direction == 'buy' else "'sell'")).fetchone()[0]
    connection.close()
    return result if result else 0

