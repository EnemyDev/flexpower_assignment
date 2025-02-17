import sqlite3
from pathlib import Path

database_file = Path(__file__).parent.absolute() / "../../data/raw/trades.sqlite"

def format_result(sql_result):
    result = []
    for row in sql_result:
        result.append({"strategy":row[0],
                       "pnl": row[1]})
    return result

def all_strategy_pnl():
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    result = cursor.execute("""
    SELECT 
        strategy,
        SUM(
            CASE 
                WHEN side = 'sell' THEN quantity * price
                WHEN side = 'buy' THEN -quantity * price
                ELSE 0
            END
        ) as total_pnl
    FROM 
        epex_12_20_12_13
    GROUP BY 
        strategy
    """).fetchall()
    connection.close()
    return format_result(result) if result else None

def strategy_pnl(strategy_id: str) -> float:
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    result = cursor.execute("""
        SELECT SUM(
            CASE 
                WHEN side = 'sell' THEN quantity * price
                WHEN side = 'buy' THEN -quantity * price
                ELSE 0
            END
        ) FROM epex_12_20_12_13 WHERE strategy = ?
    """, (strategy_id,)).fetchone()[0]
    connection.close()
    return result if result else 0