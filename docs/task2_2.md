# Task 2.2
## Results
- We can see nice "bell-curve" on chart for PV forecast, "obviously" following the day/night cycle. The DayAhead forecast is lower (especialy in peak time around 12:00) the Intraday forecast
- Wind forecast is more stable with slight dropdown around 10:00 The wind forecast has lower intraday forecasts the DayAhead forecasts
## Visualisation
- By Hour
  ![Hourly](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/average_productions/forecast_averages.png?raw=true)
- By QuarterHour
  ![Quarter-Hourly](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/average_productions/forecast_averages_15min.png?raw=true)
## Assumptions
- The bell-curve on chart for PV forecast can help predict most usually available volume from PV production as well, and point, to times around 12:00 to buy on DayAhead contract and sell on intraday contract, while wind forecast is in theory showing opportunity to buy on intraday and sold on DayAhaed contract if my assumption is correct. (Would require backtest to confirm this assumption.) 
