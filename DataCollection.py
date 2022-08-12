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
import matplotlib
matplotlib.use('QT5Agg')

# Create a Stratey
class DataCollection():
    def collectData(self, cerebro):
        
        datalist = [
            ('C:/Users/arikaufm/Documents/BacktraderSample/datas/V.csv', 'Visa'),
            ('C:/Users/arikaufm/Documents/BacktraderSample/datas/MA.csv', 'Mastercard')
        ]

        for i in range(len(datalist)):
            data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
            cerebro.adddata(data, name=datalist[i][1])


