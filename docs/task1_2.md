# Task 1.2
For this solution I did again used SQL query: 
``` 
"SELECT SUM(
            CASE 
                WHEN side = 'sell' THEN quantity * price
                WHEN side = 'buy' THEN -quantity * price
                ELSE 0
            END
        ) FROM epex_12_20_12_13 WHERE strategy = ?", (strategy_id)
        