import cvxportfolio as cp


class MomentumAlpha(cp.ReturnsForecast):

    def __init__(self, returns, window):
        """

        :param returns: historical returns
        :param window: momentum look-back window
        """
        returns = returns.rolling(window, min_periods=window).mean().dropna(how='all')  # .shift(1) if no cheating
        super(MomentumAlpha, self).__init__(returns)
