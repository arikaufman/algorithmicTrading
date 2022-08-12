# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 11:06:25 2022

@author: arikaufm
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt


# Collect Data (Pairs Trading requires two data streams, the rest require one data stream.)
class DataCollection():
    def collectData(self, cerebro):

        datalist = [
            ('C:/Development/algorithmicTrading/datas/V.csv', 'Visa'),
            ('C:/Development/algorithmicTrading/datas/MA.csv', 'Mastercard')
        ]

        for i in range(len(datalist)):
            data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
            cerebro.adddata(data, name=datalist[i][1])


