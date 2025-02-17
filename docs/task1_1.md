# Task 1.1
We can use sql query to determine the volume : 
```
"SELECT SUM(quantity) FROM epex_12_20_12_13 WHERE side = " +("'buy'" if direction == 'buy' else "'sell'")