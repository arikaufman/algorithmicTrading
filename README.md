# algorithmicTrading
Experimenting with Algo Trading using Backtrader Python Module.

## Table of Contents
[1 File Structure Information](#File-Structure-Information)  
[2 Pairs Trading](#Pairs-Trading)  
[2.1 Background](#Background)  
[2.2 Experimentation](#Experimentation)   

## File Structure Information:
### main.py 
Takes in a strategy class, a data collection class, and sets the broker cash amount, stake, and commission. It also displays the plot of both the data and trading style, along with the analysis values themselves. In main.py, feel free to edit the:
* Strategy added to the cerebro instance ```cerebro.addstrategy(StrategyToTry)```
* The desired cash amount to test with  ``` cerebro.broker.setcash(Amount) ```
* The commission percentage per trade ``` cerebro.broker.setcommission(commissionAmount) ```

### common/DataCollection
The data used is collected by downloading from yahoo finance. For instance, for the oracle data, the following link was used: https://ca.finance.yahoo.com/quote/ORCL/history?p=ORCL&.tsrc=fin-srch . Ensure that the strategy you pick corresponds to the data that you are using, as the data used in DataCollection will be automatically ingested into the cerebro broker instance, per line 14 in main.py. If you'd like to improve the functionality or specificity of the data collected, feel free to edit the collectData function, that is called in main.py.

### strategies
The strategy in the strategies folder is what should be primarily changed for experimentation, and the layout of these strategies are shown in SimpleMovingAverage, BuyAndHold, and PairsTrading. Begin with SimpleMovingAverage, and BuyAndHold to get a feel for the code and how the module itself works. Here is a link to the Backtrader documentation which is also quite helpful to understand the module and code flow: https://www.backtrader.com/docu/.
We will now move on to the main experimentation done, which was in pairs Trading.

## Pairs Trading
### Background
Pairs trading is a strategy for heding of risk, which involves mathing of the short person with the long position in two underlying securities with a high positive correlation. This offseting of the long and short position is the basis for hedging, and provides profits even with market neutrality. 

The basis of this model is high correlation between the two underlying securities. Thus, the first thing done was to determine correlations between different securities in the same sectors. Once a pair of stocks is identified, whenever the two stocks appear to no longer be correlated, the overpriced stock is shorted, and the undervalued security is bought, assuming that they will come back to the mean correlation, and profit can be made on the mean-reversion. There are two ways to identify this temporary lack of correlation. Either by purely checking the correlation, or using cointegration.

At first, I tried incrementally deducing Pearson's Coefficients for different pairs of securities as shown in the ```DataPreProcessing.py``` file. This would yield results like the following: 
INSERT IMAGE
When this was inserted into my model, however, I was obtaining strange results, and the correlated stocks were not always mean reverting. I did a bit more reading and found that I should be using cointegration to deduce my security pairs.

Correlation shows the linear association between two random variables, or bivariate data. In contrast, two sets of variables are cointegrated, if a linear combination of those variables has a lower order of integration. If a linear combination of the collection is integrated of order less than d ( Where d is the individual series integrations), a set is said to be cointegrated. Cointegration is far more powerful than corrrelation, as it avoids the possibility of spurious correlation. This is when two or more events/variables are associated, but not casually related, due to coincidence, or the presence of a third, unseen variable.

Thus, instead, I ran the Dicky Fuller test on the spread, gives pValue as the result. If the pValue was less than 0.05 we can say with 95% conidence that the securities are cointegrated. The results of this test is shown below:
INSERT IMAGE

Now, I can obtain securities with high cointegration, and use the pairs trading model to indetifiy entry and exit points. The model I built builds an ordinary least squares regression between the two securities in question. When the model has a positive z-score above an upper limit, you should short stock 1, and buy stock 2, selling out when the upper-limit band is reached (and we've reached mean-reversion). In contrast, when the model has a negative z-score below a lower limit, you should short stock 2, and buy stock 1, selling out when the lower-limit band is reached (and we've reached mean-reversion).

### Parameter Tuning
With no parameter tuning, the following data was obtained:
INSERT IMAGE OF FIRST RUN NO PARAMETER TUNING

### Position Sizing

### Further Thoughts
