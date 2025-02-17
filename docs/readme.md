# Tasks Bried description
- **Please see MD files in this directory for each task.**
---
# Research, Ideas, Next steps/Personal TODO
## Additional research
### Histograms and Gauss standard distribution theory
- in POC folder is located script, that generate multiple histogram charts in order to find standard distribution curve (bell-curve) and help with next assumption while finding proffitable trading strategies.
- The resulting charts also works with mean, modus and median:
  - Modus bar is highlighted red. This basicly highlight the most probable price in given context.
  - Bars between mean to median are highlighted yellow as well as vertical lines are plotted. This area is usualy used in statistics as it represents 2 ways of finding "midpoint" in data-sample. 
  - In Legend of charts, we also see the stdiv and probabilities of price holding in given areas based on Gauss standard distribution theory, what can be used to find "annomaly" situations ad trade towards correction
- Theese charts may be reviewed in oreder to find "most clean correlation factors" in form of clean "Bellcurve" and build strategy rulesets arround.
- In order to fully utilize theese charts, it would be ideal to transfer the data into databse, and craft interactive interface allowing advanced filtering based on all available options, in order to find current market context.
### Markov process
- again in POC folder is located script apply markov process over quaeters of hour, looking for probabilities of specific sequence of quartels directions forming hour
- This approach can be used with **"process of elimination"** to predict probabilities of 3rd or 4th quarter of hour.
  - Example result:
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
## Additional ideas
- It would be interesting to review orderbook and volume as well
## Next Steps/TODO
### Bugfixing/unfinished code
- Fix the quarterly optimized battery strategy and EQ plots related to it.
- Go over @TODO comments in code.
- Extend DA vs ID strategies with metrics display like battery strategy (Bug occured when rewriting from POC to system) 
### Different approach for DA vs ID strategies
- Instead of buying each hour, what was pointe4d in simple strat based on average DA vs ID prices, we may use each hour historical probability of price to calculate EV, and trade based on EV, that comparing results with simple approach
- Manually review all histograms and try to find strategy
  - Strategy maybe waiting for "annomaly values" and trade towards the mean-median or modus area.
- Make strategy based on markov process results,
  - Itendifying curren sequence after 2nd quartel of hour and by applying process of elimination, trading 3rd and 4th hourly quarters in more probable direction
  - Additionaly implement EV as well here.