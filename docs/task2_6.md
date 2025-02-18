# Task 2.6
## Process
- First simple aproach 
  - finding 3 hours with average highest and 3 hours with lowest average price, making all combinations
  - all 9 combinations of charge/discharge times are then backtested, and the results are shown on interactive chart as well as saved in ```/data/processed/``` folders, along with csv files containing all trades.
- Seasonal aproach 
  - The results of first 9 combinations is compared on 3months (quartel) bases, in order to reflect the seasonality. (This feature is currently under debug, as results got broken during refractor from POC) 
## Results 
### Visualisation
- Using DayAhead price
    ![DayAhead price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/battery/9_best_times_DayAheadPriceHourlyEURMWh_eq.png?raw=true)
- Using IntraDay price
    ![IntraDay price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/battery/9_best_times_IntradayPriceHourlyEURMWh_eq.png?raw=true)
### Text summary
- *The results for second approach was generated with POC code*
```
Strategy (DayAheadPriceHourlyEURMWh): Charge 3:00 - Discharge 19:00
  Maximum Win Streak: 304
  Maximum Lose Streak: 2
  Total Wins: 357
  Total Losses: 7
  Final Cumulative Profit: 1969544.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 3:00 - Discharge 18:00
  Maximum Win Streak: 342
  Maximum Lose Streak: 2
  Total Wins: 356
  Total Losses: 9
  Final Cumulative Profit: 1894458.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 3:00 - Discharge 8:00
  Maximum Win Streak: 276
  Maximum Lose Streak: 4
  Total Wins: 343
  Total Losses: 22
  Final Cumulative Profit: 1728580.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 4:00 - Discharge 19:00
  Maximum Win Streak: 304
  Maximum Lose Streak: 2
  Total Wins: 357
  Total Losses: 8
  Final Cumulative Profit: 1928421.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 4:00 - Discharge 18:00
  Maximum Win Streak: 404
  Maximum Lose Streak: 2
  Total Wins: 358
  Total Losses: 7
  Final Cumulative Profit: 1853335.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 4:00 - Discharge 8:00
  Maximum Win Streak: 276
  Maximum Lose Streak: 4
  Total Wins: 349
  Total Losses: 16
  Final Cumulative Profit: 1687457.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 2:00 - Discharge 19:00
  Maximum Win Streak: 280
  Maximum Lose Streak: 2
  Total Wins: 354
  Total Losses: 10
  Final Cumulative Profit: 1888702.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 2:00 - Discharge 18:00
  Maximum Win Streak: 314
  Maximum Lose Streak: 4
  Total Wins: 352
  Total Losses: 12
  Final Cumulative Profit: 1814390.00

Strategy (DayAheadPriceHourlyEURMWh): Charge 2:00 - Discharge 8:00
  Maximum Win Streak: 110
  Maximum Lose Streak: 4
  Total Wins: 326
  Total Losses: 38
  Final Cumulative Profit: 1649274.00

Quarter 2021Q1: Best Strategy (DayAheadPriceHourlyEURMWh) - Charge at 3:00, Discharge at 18:00
Quarter 2021Q2: Best Strategy (DayAheadPriceHourlyEURMWh) - Charge at 3:00, Discharge at 19:00
Quarter 2021Q3: Best Strategy (DayAheadPriceHourlyEURMWh) - Charge at 3:00, Discharge at 19:00
Quarter 2021Q4: Best Strategy (DayAheadPriceHourlyEURMWh) - Charge at 3:00, Discharge at 18:00

Best Quarterly Strategy Metrics (DayAheadPriceHourlyEURMWh):
  Maximum Drawdown: 31755.00
  Maximum Runup: 2106237.00
  Maximum Win Streak: 342
  Maximum Lose Streak: 2
  Total Wins: 361
  Total Losses: 3
  Final Cumulative Profit: 2101945.00


Strategy (IntradayPriceHourlyEURMWh): Charge 3:00 - Discharge 19:00
  Maximum Win Streak: 254
  Maximum Lose Streak: 2
  Total Wins: 358
  Total Losses: 7
  Final Cumulative Profit: 1929010.00

Strategy (IntradayPriceHourlyEURMWh): Charge 3:00 - Discharge 18:00
  Maximum Win Streak: 312
  Maximum Lose Streak: 4
  Total Wins: 354
  Total Losses: 11
  Final Cumulative Profit: 1836358.00

Strategy (IntradayPriceHourlyEURMWh): Charge 3:00 - Discharge 8:00
  Maximum Win Streak: 236
  Maximum Lose Streak: 4
  Total Wins: 346
  Total Losses: 19
  Final Cumulative Profit: 1737331.00

Strategy (IntradayPriceHourlyEURMWh): Charge 4:00 - Discharge 19:00
  Maximum Win Streak: 188
  Maximum Lose Streak: 2
  Total Wins: 358
  Total Losses: 7
  Final Cumulative Profit: 1900564.00

Strategy (IntradayPriceHourlyEURMWh): Charge 4:00 - Discharge 18:00
  Maximum Win Streak: 188
  Maximum Lose Streak: 4
  Total Wins: 353
  Total Losses: 12
  Final Cumulative Profit: 1807912.00

Strategy (IntradayPriceHourlyEURMWh): Charge 4:00 - Discharge 8:00
  Maximum Win Streak: 236
  Maximum Lose Streak: 4
  Total Wins: 351
  Total Losses: 14
  Final Cumulative Profit: 1708885.00

Strategy (IntradayPriceHourlyEURMWh): Charge 2:00 - Discharge 19:00
  Maximum Win Streak: 166
  Maximum Lose Streak: 2
  Total Wins: 350
  Total Losses: 14
  Final Cumulative Profit: 1850429.00

Strategy (IntradayPriceHourlyEURMWh): Charge 2:00 - Discharge 18:00
  Maximum Win Streak: 182
  Maximum Lose Streak: 6
  Total Wins: 349
  Total Losses: 15
  Final Cumulative Profit: 1759396.00

Strategy (IntradayPriceHourlyEURMWh): Charge 2:00 - Discharge 8:00
  Maximum Win Streak: 124
  Maximum Lose Streak: 4
  Total Wins: 334
  Total Losses: 30
  Final Cumulative Profit: 1660801.00

Quarter 2021Q1: Best Strategy (IntradayPriceHourlyEURMWh) - Charge at 3:00, Discharge at 18:00
Quarter 2021Q2: Best Strategy (IntradayPriceHourlyEURMWh) - Charge at 3:00, Discharge at 19:00
Quarter 2021Q3: Best Strategy (IntradayPriceHourlyEURMWh) - Charge at 3:00, Discharge at 19:00
Quarter 2021Q4: Best Strategy (IntradayPriceHourlyEURMWh) - Charge at 3:00, Discharge at 18:00

Best Quarterly Strategy Metrics (IntradayPriceHourlyEURMWh):
  Maximum Win Streak: 312
  Maximum Lose Streak: 2
  Total Wins: 361
  Total Losses: 4
  Final Cumulative Profit: 2075726.00

Comparison of DA vs ID Prices:
Best_annual Strategy:
  Profit Difference (ID - DA): -40534.00
  Better Market: Day-Ahead

Best_quarterly Strategy:
  Profit Difference (ID - DA): 0.00
  Better Market: Equal
```