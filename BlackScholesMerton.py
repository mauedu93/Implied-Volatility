import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
import quandl
import yfinance as yf
import scipy.stats as st

quandl.ApiConfig.api_key = 'JMxryiBcRV26o9r5q7uv'


class BlackScholesModel:
    def __init__(self, exp_date, today_date, stock_price, strike, implied_vol):
        self.exp_date = exp_date
        self.today_date = today_date
        self.stock_price = stock_price
        self.strike = strike
        self.implied_vol = implied_vol

    def maturity(self):
        maturity_d = (self.exp_date - self.today_date).days
        maturity = maturity_d / 365
        return maturity

    def risk_free(self):
        num_days = [30, 60, 90, 180, 365, 730, 1095, 1825, 2555, 3650, 7300, 10950]
        yield_curve = quandl.get("USTREASURY/YIELD", authtoken='JMxryiBcRV26o9r5q7uv')
        rf_ttm = list(yield_curve.columns)
        risk_free = []
        if round(self.maturity()*365) < 0:
            return "Expire date must be greater than today"
        elif round(self.maturity()*365) > num_days[-1]:
            return yield_curve[rf_ttm[-1]][-1] / 100
        else:
            for b, f in zip(num_days, rf_ttm):
                if round(self.maturity()*365) < b:
                    risk_free.append(yield_curve[f][-1] / 100)
            return risk_free[0]

    def norm_d1(self):
        d1 = (np.log(self.stock_price / self.strike) + (self.risk_free() + (np.power(self.implied_vol, 2) / 2) *
                                                        self.maturity())) / (
                     self.implied_vol * math.sqrt(self.maturity()))
        norm_d1 = st.norm.cdf(d1)
        return d1, norm_d1

    def norm_d2(self):
        d1 = self.norm_d1()[0]
        d2 = d1 - self.implied_vol * math.sqrt(self.maturity())
        norm_d2 = st.norm.cdf(d2)
        return norm_d2

    def call_price(self):
        d1, norm_d1 = self.norm_d1()
        call_price = (self.stock_price * norm_d1 - (self.strike *
                                                    math.exp(
                                                        -self.risk_free() * self.maturity()) * self.norm_d2()))
        return call_price

    def bsm_callp(self, CallP):
        dif = CallP - self.call_price()
        return dif


    def callp_plot(self, n_rows, n_col, figure_size, subtitle=None):

        if not isinstance(figure_size, (list, tuple)):
            print("Figure size has to be Tuple or List with the width and the height")
            return

        fig, axs = plt.subplots(n_rows, n_col, figsize=figure_size)

        if subtitle is None:
            name = yf.Ticker('^GSPC').info['shortName']
            fig.suptitle(f'{name} Call Value vs. Strike Price', fontsize=18, fontweight='bold')
        else:
            fig.suptitle(subtitle, fontsize=18, fontweight='bold')
        i, j = 0, 0

        if isinstance(self.exp_date, datetime.datetime):

            axs.plot(self.strike[self.exp_date],
                     self.call_price()[self.exp_date],
                     'tab:red',
                     linewidth=4.0,
                     label='BSM model')  # Plots the first expiration based on BSM model
            axs.plot(self.strike[self.exp_date],
                     yf.Ticker('^GSPC').option_chain(self.exp_date).calls['lastPrice'],
                     'tab:cyan',
                     linewidth=1.0,
                     label='Market price')  # Plots the first expiration based on actual market price
            axs.legend(labelspacing=2, borderpad=1.25, fontsize=10)  # Set legend
            axs.set_xlim(xmin=0.0)  # To start the graph on (0,0)
            axs.set_ylim(ymin=0.0)
            axs.set_xlabel("Strike Price", fontsize=14)  # Set X-axis label
            axs.set_ylabel("Call Price", fontsize=14)  # Set Y-axis label
            axs.set_title(f"Expiration: {datetime.strptime(self.exp_date, '%Y-%m-%d').strftime('%b %d, %Y')}",
                          fontsize=14)  # Subtitle on the first figure
            axs.spines['right'].set_visible(False)  # Remove right border on the first subplot
            axs.spines['top'].set_visible(False)  # Remove top border on the first subplot

        else:

            for n in (0, len(self.exp_date) - 1):

                if n_rows == 1:
                    ax = axs[j]
                elif n_col == 1:
                    ax = axs[i]
                else:
                    ax = axs[i, j]

                ax.plot(self.strike[self.exp_date[n]],
                        self.call_price()[self.exp_date[n]],
                        'tab:red',
                        linewidth=4.0,
                        label='BSM model')  # Plots the first expiration based on BSM model
                ax.plot(self.strike[self.exp_date[n]],
                        yf.Ticker('^GSPC').option_chain(self.exp_date[n]).calls['lastPrice'],
                        'tab:cyan',
                        linewidth=1.0,
                        label='Market price')  # Plots the first expiration based on actual market price
                ax.legend(labelspacing=2, borderpad=1.25, fontsize=10)  # Set legend
                ax.set_xlim(xmin=0.0)  # To start the graph on (0,0)
                ax.set_ylim(ymin=0.0)
                ax.set_xlabel("Strike Price", fontsize=14)  # Set X-axis label
                ax.set_ylabel("Call Price", fontsize=14)  # Set Y-axis label
                ax.set_title(f"Expiration: {datetime.strptime(self.exp_date[n], '%Y-%m-%d').strftime('%b %d, %Y')}",
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
