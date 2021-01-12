#Implied Volatility

The implied volatility is a measure of market risk and helps determine changes in the supply and demand of securities; however, the implied volatility does not provide the direction of the change. The implied volatility can be calculated from option prices using the Black-Scholes formula. This metric gives a forward-looking perspective to the analyst. When the market is bearish, the volatility tends to increase; on the other hand, when investors expect prices to rise, the implied volatility tends to fall.

This notebook will provide an algorithm to calculate the implied volatility for a given asset using its call-option chain. The algorithm first retrieves the variables needed to calculate the call price with the Black-Scholes model without dividend payment. Then, the algorithm estimates the spread between the calculated call price and the actual market price. Finally, the algorithm finds the implied volatility that makes the square differences closest to zero.

