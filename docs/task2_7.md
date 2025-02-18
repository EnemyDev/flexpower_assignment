# Task 2.7
## Process
### Simple approach
- Finding hours, where average DA hourly price is lower then intraday hourly price. 
### ML aproach
- This strategy uses machine learning to predict when to go long based on time, day, and renewable production.
- It considers buying on day-ahead if the prediction suggests intraday prices will be higher, with a 100 MW position.
- Factors like hour, day of week, and total renewable production are used to inform these decisions.
- The model's accuracy gives an idea of how well historical patterns predict future price movements.
- Real-world application would need to account for transaction costs, market impact, and further variables. and also bigger dataset
- **As the dataset provided contained only 1 year of data, I did split the data in half and used first half of the year for training, and second half of year for backtesting, what disallow me to test "seasonality" based on month**
## Results
### Simple approach
- After running, we can see the strategy did basicaly kept buying on DayAhead and selling on IntraDay 100MWH and resulted in 4055652.0
![Simple strategy EQ curve](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/da_id/DA_ID_Simple.png?raw=true)
### ML aproach
- The ML strategy did result in 1801790.0 profit for half-year period. The larger datasaet, may allow to optimize for seasonalities, what may allow us to elaborate on this model further
![Simple strategy EQ curve](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/da_id/DA_ID_ML.png?raw=true)
- As we do see nice runups in EQ curve, but also strong dip-downs, we may implement "risk-profile" for position sizing. 
- Overall results of this strategy are positive but not overperforming simple approach with same position sizing, therefor it needs to be investigated further.

### Summary

- In order to compare 2 used strategies, we generated chart with both eq curves over same time period (second half of the year).
    ![Simple vs ML EQ curve](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/da_id/simple_vs_ml.png?raw=true)
    - We can see that the ML strategy avoided strong digdown during october, but did not score same runup in november. It can point the seasonal tendencies of both strategies, and may be considered in risk profiling (position sizing)
    - Overal ML strategy is "safer" in terms of drawdowns but provide less income.
- **If we put "smoothness" of ML curve into consideration, we can can use larger position sizing with ML strategy, and potentionaly "outplay" the simple strategy**