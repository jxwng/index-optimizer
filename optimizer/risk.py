import cvxportfolio as cp


class HistCovRiskModel(cp.FullSigma):

    def __init__(self, returns, window):
        """

        :param returns: historical returns
        :param window: look-back window to calculate historical quadratic covariance
        """
        sigma = returns.rolling(window=window, min_periods=window).cov().dropna().droplevel(1)
        super(HistCovRiskModel, self).__init__(sigma)
