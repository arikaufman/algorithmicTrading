# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader.analyzers as btanalyzers

# Create a Stratey
class AnalyzerSuite():
    def defineAnalyzers(self, cerebro):
        cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
        cerebro.addanalyzer(btanalyzers.Returns, _name='myreturn')

    def returnAnalyzers(self, thestrats):
        thestrat = thestrats[0]
        return {'DrawDown': thestrat.analyzers.mydrawdown.get_analysis()['max']['drawdown'],
                'Sharpe Ratio:': thestrat.analyzers.mysharpe.get_analysis()['sharperatio'],
                'Returns:': thestrat.analyzers.myreturn.get_analysis()['rnorm100']}
