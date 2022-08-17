# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 11:06:25 2022

@author: arikaufm
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths

# Import the backtrader platform
import backtrader as bt

# Collect List of Datas
class DataCollection():
    def collectData(self, cerebro):
        datalist = [
            ('C:/Development/algorithmicTrading/datas/WTI2012022.csv', 'WTI'),
            ('C:/Development/algorithmicTrading/datas/BRNT.L20122022.csv', 'BRNT.L')
        ]

        for i in range(len(datalist)):
            data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
            cerebro.adddata(data, name=datalist[i][1])


