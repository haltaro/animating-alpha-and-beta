#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  MIT License
#
#  Copyright (c) 2017 haltaro
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Author: haltaro <github.com/haltaro>
#  Reseacher in a Japanese company. His reseach interests are related to
#  network architectures, protocols, traffic control, mathematical modeling,
#  optimization, machine learning, and shiba dog :-)
#
#  NOTE:
#  udacity.get_data(), udacity.fill_missing_values(), and
#  udacity.compute_daily_returns() are functions defined in
#  "Machine learning for trading" at Udacity:
#  https://www.udacity.com/course/machine-learning-for-trading--ud501


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.cm as cm
import udacity  # Functions defined in "Machine learning for trading"


def animate_a_b(
        symbols=["AAPL", "GOOG", "MSFT", "BRK-A", "AMZN",
                 "FB", "XOM", "JNJ", "JPM", "WFC"],
        start_date="2006-12-01", end_date="2016-12-01",
        period=252 * 2):

    """ --- Preprocess: You have to take Udacity! --- """
    # Read data
    dates = pd.date_range(start_date, end_date)  # date range as index
    stock_data = udacity.get_data(symbols, dates)  # get data for each symbol

    # Fill missing values
    udacity.fill_missing_values(stock_data)
    # Daily returns
    daily_returns = udacity.compute_daily_returns(stock_data)

    """ --- Make animation --- """
    interval = 10  # Nframe interval
    frames = (len(stock_data) - period) / interval  # Num of frames
    markers = ["o", "^", "s"]

    def animate_polyfit(nframe):

        plt.clf()
        daily_returns_p = daily_returns[
            nframe * interval: nframe * interval + period]
        corr = daily_returns_p.corr(method="pearson")

        xmin, xmax = -0.003, 0.003
        ymin, ymax = 0.0, 2.0

        plt.plot([0, 0], [ymin, ymax], '--', color='black')
        plt.plot([xmin, xmax], [1, 1], '--', color='black')
        for n, symbol in enumerate(symbols[1:]):
            beta, alpha = np.polyfit(daily_returns_p["SPY"],
                                     daily_returns_p[symbol], 1)
            plt.plot(alpha, beta, markers[n % len(markers)], alpha=0.7,
                     label=symbol, color=cm.jet(n * 1. / len(symbols)),
                     ms=np.absolute(corr.ix[0, n + 1]) * 25)
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
        plt.xlabel("Alpha")
        plt.ylabel("Beta")
        plt.text(xmax, ymax, str(daily_returns_p.index[-1]),
                 ha="right", va="bottom")
        plt.legend(loc="upper left")

    fig = plt.figure(figsize=(8, 8))
    anim = ani.FuncAnimation(fig, animate_polyfit, frames=frames)
    anim.save("ab.gif", writer="imagemagick", fps=18)


if __name__ == "__main__":
    animate_a_b()
