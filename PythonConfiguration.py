# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:57:03 2022

@author: arikaufm
"""

import backtrader as bt
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Testing bt and cerebro instantiation
    cerebro = bt.Cerebro()
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    
    # Testing matplotlib/numpy
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.grid()
    plt.show()