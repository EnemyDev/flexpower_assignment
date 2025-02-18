# Tasks Brief description
- **Please see MD files in this directory for each task.**
---
# Additional research
## Histograms and Gauss standard distribution theory
- in POC folder is located script, that generate multiple histogram charts in order to find standard distribution curve (bell-curve) and help with next assumption while finding proffitable trading strategies. 
  
  *All histograms also saved in ```/docs/hisgorams/``` folder*
- The resulting charts also works with mean, modus and median:
  - Modus bar is highlighted red. This basicly highlight the most probable price in given context.
  - Bars between mean to median are highlighted yellow as well as vertical lines are plotted. This area is usualy used in statistics as it represents 2 ways of finding "midpoint" in data-sample. 
  - In Legend of charts, we also see the stdiv and probabilities of price holding in given areas based on Gauss standard distribution theory, what can be used to find "annomaly" situations ad trade towards correction
- Theese charts may be reviewed in oreder to find "most clean correlation factors" in form of clean "Bellcurve" and build strategy rulesets arround.
- In order to fully utilize theese charts, it would be ideal to transfer the data into databse, and craft interactive interface allowing advanced filtering based on all available options, in order to find current market context.
- ### Example (Battery charge/discharge hours):
  - Best battery charge hour on histogram:
    ![IntraDay price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/histograms/IntradayPriceHourly_Hour_3.png?raw=true)
    - We can observe Normal Distribution chart that is little scewed.
    - The modus meeting the High of bellcurve
    - Mean and median showing only ~10Eur spread (favoring less volatility during this time)
    - The modus is on left side of mean-median range, what favor lower prices in standard distribution days
    - Curve is little scewed to the right
  - Best battery discharge hour ohn histogram:
    ![IntraDay price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/histograms/IntradayPriceHourly_Hour_19.png?raw=true)
    - Discharge chart is not showing as clean distribution chart as previous example, but we can see Non-symetric bymodal distribution forming (2 bellcurves of different sizes) (favoring more volatility during this time)
    - The modus position formed below the first peak of bell curve but still above charge hour modus.
    - Median-mean range showing 3times bigger spread then charge hour, but still formed above theese values from charge hour
  - **All 3 values of discharge hour (modus, median, mean) formed above charge hour values confirming statistical edge.**
  - **The observation of bymodal distribution chart is favorable, as its pointing for potential "peaks" in energy pricing during discharge hours**
- ### Example2 (Seasonality and volatility):
  - June prices:
    ![June price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/histograms/IntradayPriceHourly_Month_June.png?raw=true)
    - We can observe Normal Distribution chart as well as all 3 values (modus, median, mean) pointing out the peak of it.
    - The Gauss std Deviation size, is also pointing to less volatility during June as well
  - December prices:
    ![December price](https://github.com/EnemyDev/flexpower_assignment/blob/main/docs/histograms/IntradayPriceHourly_Month_December.png?raw=true)
    - On December chart, we cannot observer clean distribution pattern
    - The mean and median values are lacated at peak of the chart
    -  The distance of mean/median from mode, as well as size of Gauss stdiv favoring more volatility in pricing of energy during December
  - **Comparism of theese 2 charts confirms seasonality in markets. There can be multiple explanations**
    - PV Production during winter are much lower then during summer periods
      - Many obvious and scientific reasons (sunrise-sunset period, temperature for effectivity of solar panels, snow on solar panels, etc.)
    - Demand during winter for energy is higher then during summer periods
      - Heating requirements
      - More "light" hours due to smaller sunrise sunset period
      - *Overall more "indoor" orientated activites*
## Markov process
- again in POC folder is located script apply markov process over quaeters of hour, looking for probabilities of specific sequence of quartels directions forming hour
- This approach can be used with **"process of elimination"** to predict probabilities of 3rd or 4th quarter of hour.
  - Advanced combination filtering of dataset based on month, day of week, and current hour should be implemented before looking for strategy
  - Example of simple result:
  ```
  Probabilities for transitions from B:
    B -> B: 42.68%
    B -> S: 57.31%
    B -> N: 0.01%

  Probabilities for transitions from S:
    S -> B: 51.91%
    S -> S: 48.05%
    S -> N: 0.04%

  All 4-Quarter Sequences Starting from Bullish:
    BBBB: 7.77%
    BBBS: 10.44%
    ...
    BBSB: 12.70%
    BBSS: 11.75%
    ...
    BSBB: 12.70%
    BSBS: 17.05%
    BSSB: 14.30%
    BSSS: 13.23%
    ...
  All 4-Quarter Sequences Starting from Bearish:
    SBBB: 9.45%
    SBBS: 12.70%
    ...
    SBSB: 15.44%
    SBSS: 14.30%
    ...
    SSBB: 10.65%
    SSBS: 14.30%
    ...
    SSSB: 11.99%
    SSSS: 11.10%
    ...
  ```
# Additional ideas
- It would be interesting to review orderbook and volume as well
# Next Steps/TODO
## Bugfixing/unfinished code
- Fix the quarterly optimized battery strategy and EQ plots related to it.
- Go over @TODO comments in code.
- Extend DA vs ID strategies with metrics display like battery strategy (Bug occured when rewriting from POC to system) 
## Different approach for DA vs ID strategies
- Instead of buying each hour, what was pointed in simple strat based on average DA vs ID prices, we may use each hour historical probability of price to calculate EV, and trade based on EV, then comparing results with simple approach
- Manually review all histograms and try to find strategy
  - Strategy maybe waiting for "annomaly values" and trade towards the mean-median or modus area.
- Implement additional filters and make strategy based on markov process results,
  - Itendifying curren sequence after 2nd quartel of hour and by applying process of elimination, trading 3rd and 4th hourly quarters in more probable direction
  - Additionaly implement EV as well here.