from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import strategies.PairsTradingStrategy as Pairs
import common.AnalyzerSuite as AnalyzerSuite
import common.DataCollection as DataCollection

if __name__ == '__main__':
    # ------------------------------------------------------------------------------------
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    cerebro.addstrategy(Pairs.PairsTradingStrategy)
    DataCollection.DataCollection.collectData(DataCollection, cerebro)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    # Set the commission
    #cerebro.broker.setcommission(commission=0.001)

    # ------------------------------------------------------------------------------------

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Analyzer
    AnalyzerSuite.AnalyzerSuite.defineAnalyzers(AnalyzerSuite, cerebro)
    # Run over everything
    thestrats = cerebro.run(stdstats=True)

    # -----------------------------------------------------------------------------------

    print(AnalyzerSuite.AnalyzerSuite.returnAnalyzers(AnalyzerSuite, thestrats))
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result
    cerebro.plot()