# import os

import quandl

import numpy as np

import math

import scipy.stats as st

quandl.ApiConfig.api_key = 'JMxryiBcRV26o9r5q7uv'


class BlackScholesModel:
    def __init__(self, stock_price, strike, risk_free, maturity, implied_vol, call_price):
        self.stock_price = stock_price
        self.strike = strike
        self.risk_free = risk_free
        self.maturity = maturity
        self.implied_vol = implied_vol
        self.call_price = call_price

    def maturity(self, exp_date, today):
        self.maturity = (exp_date - today).days
        return self.maturity

    def risk_free(self, exp_date, today):
        num_days = [30, 60, 90, 180, 365, 730, 1095, 1825, 2555, 3650, 7300, 10950]
        yield_curve = quandl.get("USTREASURY/YIELD", authtoken='JMxryiBcRV26o9r5q7uv')
        rf_ttm = list(yield_curve.columns)
        self.risk_free = []
        if round(self.maturity(exp_date, today)) < 0:
            return "Expire date must be greater than today"
        elif round(self.maturity(exp_date, today)) > num_days[-1]:
            return yield_curve[rf_ttm[-1]][-1] / 100
        else:
            for b, f in zip(num_days, rf_ttm):
                if round(self.maturity(exp_date, today)) < b:
                    self.risk_free.append(yield_curve[f][-1] / 100)
            return self.risk_free[0]

    def _norm_d1(self, s, k, r, t, sigma):
        d1 = (np.log(s/k) + (r + (np.power(sigma, 2) / 2) * t)) / (sigma * math.sqrt(t))
        n_d1 = st.norm.cdf(d1)
        return d1, n_d1

    def _norm_d2(self, d1, sigma, t):
        d2 = d1 - sigma * math.sqrt(t)
        n_d2 = st.norm.cdf(d2)
        return n_d2

    def call_price(self, s, k, r, t, sigma):
        d1, n_d1 = self._norm_d1(s, k, r, t, sigma)
        n_d2 = _norm_d2(d1, sigma, t)
        self.call_price = S * n_d1 - k * math.exp(-r * t) * n_d2
        return self.call_price

    def callp_plot(self, n_rows, n_col, figure_size, expir_dates, subtitle=None):

        if not isinstance(figure_size, (list, tuple)):
            print("Figure size has to be Tuple or List with the width and the height")
            return

        fig, axs = plt.subplots(n_rows, n_col, figsize=figure_size)

        if subtitle == None:
            name = GSPC.info['shortName']
            fig.suptitle(f'{name} Call Value vs. Strike Price', fontsize=18, fontweight='bold')
        else:
            fig.suptitle(subtitle, fontsize=18, fontweight='bold')
        i, j = 0, 0
        for n in (0, len(expir_dates) - 1):

            if n_rows == 1:
                ax = axs[j]
            elif n_col == 1:
                ax = axs[i]
            else:
                ax = axs[i, j]

            ax.plot(K[expir_dates[n]],
                    C[expir_dates[n]],
                    'tab:red',
                    linewidth=4.0,
                    label='BSM model')  # Plots the first expiration based on BSM model
            ax.plot(K[expir_dates[n]],
                    GSPC.option_chain(expir_dates[n]).calls['lastPrice'],
                    'tab:cyan',
                    linewidth=1.0,
                    label='Market price')  # Plots the first expiration based on actual market price
            ax.legend(labelspacing=2, borderpad=1.25, fontsize=10)  # Set legend
            ax.set_xlim(xmin=0.0)  # To start the graph on (0,0)
            ax.set_ylim(ymin=0.0)
            ax.set_xlabel("Strike Price", fontsize=14)  # Set X-axis label
            ax.set_ylabel("Call Price", fontsize=14)  # Set Y-axis label
            ax.set_title(f"Expiration: {datetime.strptime(expir_dates[n], '%Y-%m-%d').strftime('%b %d, %Y')}",
                         fontsize=14)  # Subtitle on the first figure
            ax.spines['right'].set_visible(False)  # Remove right border on the first subplot
            ax.spines['top'].set_visible(False)  # Remove top border on the first subplot

            if i + 1 > n_rows - 1:
                j = j + 1
                i = 0
            else:
                i += 1
        plt.show()

        plt.close()
