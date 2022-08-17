# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 11:59:22 2022

@author: arikaufm
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime

# The above could be sent to an independent module
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import math

class PairsTradingStrategy(bt.Strategy):
    params = dict(
        period=20,
        stake=10,
        qty1=0,
        qty2=0,
        upper=2.5,
        lower=-2.5,
        up_medium=0.5,
        low_medium=-0.5,
        status=0,
        portfolio_value=100000,
        stop_loss=3.0
    )

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]


    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None

    def __init__(self):
        # To control operation entries
        self.orderid = None
        self.qty1 = self.p.qty1
        self.qty2 = self.p.qty2
        self.upper_limit = self.p.upper
        self.lower_limit = self.p.lower
        self.up_medium = self.p.up_medium
        self.low_medium = self.p.low_medium
        self.status = self.p.status
        self.portfolio_value = self.p.portfolio_value
        self.stop_loss = self.p.stop_loss

        self.sma1 = bt.indicators.SimpleMovingAverage(self.datas[0], period=50)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.datas[1], period=50)
        # Signals performed with PD.OLS :
        self.transform = btind.OLS_TransformationN(self.data0, self.data1,
                                                   period=self.p.period)
        self.zscore = self.transform.zscore

    def next(self):
        x=0
        y=0
        if self.orderid:
            return  # if an order is active, no new orders are allowed

        # Step 2: Check conditions for SHORT & place the order
        # Checking the condition for SHORT
        if (self.zscore[0] > self.upper_limit) and (self.status != 1):
            #POSITION SIZING based off SMA
            deviationOffSMA1 = math.fabs((self.data0.close[0]/self.sma1[0])-1)
            deviationOffSMA2 = math.fabs((self.data1.close[0]/self.sma2[0])-1)
            value1 = 0.6 * self.portfolio_value  # Divide the cash equally
            value2 = 0.4 * self.portfolio_value
            if deviationOffSMA1 > deviationOffSMA2:
                x = int(value1 / (self.data0.close))  # Find the number of shares for Stock1
                y = int(value2 / (self.data1.close))  # Find the number of shares for Stock2
            else:
                x = int(value2 / (self.data0.close))  # Find the number of shares for Stock1
                y = int(value1 / (self.data1.close))  # Find the number of shares for Stock2

            # Placing the order
            #print('zscore is', self.zscore[0])
            print('SELL CREATE %s, price = %.2f, qty = %d' % ("Visa", self.data0.close[0], x + self.qty1))
            self.sell(data=self.data0, size=(x + self.qty1))  # Place an order for buying x + qty1 shares
            print('BUY CREATE %s, price = %.2f, qty = %d' % ("Mastercard", self.data1.close[0], y + self.qty2))
            self.buy(data=self.data1, size=(y + self.qty2))  # Place an order for selling y + qty2 shares

            # Updating the counters with new value
            self.qty1 = x  # The new open position quantity for Stock1 is x shares
            self.qty2 = y  # The new open position quantity for Stock2 is y shares

            self.status = 1  # The current status is "short the spread"

            # Step 3: Check conditions for LONG & place the order
            # Checking the condition for LONG
        elif (self.zscore[0] < self.lower_limit) and (self.status != 2):
            #POSITION SIZING based off SMA
            deviationOffSMA1 = math.fabs((self.data0.close[0]/self.sma1[0])-1)
            deviationOffSMA2 = math.fabs((self.data1.close[0]/self.sma2[0])-1)
            value1 = 0.6 * self.portfolio_value  # Divide the cash equally
            value2 = 0.4 * self.portfolio_value
            if deviationOffSMA1 > deviationOffSMA2:
                x = int(value1 / (self.data0.close))  # Find the number of shares for Stock1
                y = int(value2 / (self.data1.close))  # Find the number of shares for Stock2
            else:
                x = int(value2 / (self.data0.close))  # Find the number of shares for Stock1
                y = int(value1 / (self.data1.close))  # Find the number of shares for Stock2

            # Place the order
            #print('zscore is', self.zscore[0])
            print('BUY CREATE %s, price = %.2f, qty = %d' % ("Visa", self.data0.close[0], x + self.qty1))
            self.buy(data=self.data0, size=(x + self.qty1))  # Place an order for buying x + qty1 shares
            print('SELL CREATE %s, price = %.2f, qty = %d' % ("Mastercard", self.data1.close[0], y + self.qty2))
            self.sell(data=self.data1, size=(y + self.qty2))  # Place an order for selling y + qty2 shares

            # Updating the counters with new value
            self.qty1 = x  # The new open position quantity for Stock1 is x shares
            self.qty2 = y  # The new open position quantity for Stock2 is y shares
            self.status = 2  # The current status is "long the spread"


            # Step 4: Check conditions for No Trade
            # If the z-score is within the two bounds, close all
        elif ((self.zscore[0] < self.up_medium and self.zscore[0] > self.low_medium)):
            order1 = self.close(self.data0)
            order2 = self.close(self.data1)
            if order1 is not None:
                print('CLOSE POSITION %s, price = %.2f' % ("Visa", self.data0.close[0]))
            if order2 is not None:
                print('CLOSE POSITION %s, price = %.2f' % ("Mastercard", self.data1.close[0]))

        

    def stop(self):
        print('==================================================')
        print('Starting Value - %.2f' % self.broker.startingcash)
        print('Ending   Value - %.2f' % self.broker.getvalue())
        print('==================================================')
