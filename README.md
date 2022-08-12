# algorithmicTrading
Experimenting with Algo Trading using Backtrader Python Module.

## File Structure Information:
main.py takes in a strategy class, a data collection class, and sets the broker cash amount, stake, and commission. It also displays the plot of both the data and trading style, along with the analysis values themselves. main.py should not be changed, besides the stake (which needs to be adjusted to fit trading algorithm) and the strategy name.

The DataCollection, and TestStrategy should be changed by each team. The data is collected by downloading from yahoo finance. For instance, for the oracle data, the following link was used: https://ca.finance.yahoo.com/quote/ORCL/history?p=ORCL&.tsrc=fin-srch . Ensure that the date time values in DataCollection correspond to the DateTime values selected in yahoo finance.

The Strategy is what should be primarily changed, and the layout of these strategies are shown in TestStrategy, TestStrategy2, and TestStrategyBenchmark. Begin with TestStrategy2 and TestStrategyBenchmark to get a feel for the code and how the module itself works. Here is a link to the Backtrader documentation which is also quite helpful to understand the module and code flow: https://www.backtrader.com/docu/.
