import cvxportfolio as cp
import cvxpy as cvx
import pandas as pd


class TurnoverLimit(cp.constraints.BaseConstraint):

    def __init__(self, max_fraction, **kwargs):
        self.max_fraction = max_fraction
        super(TurnoverLimit, self).__init__(**kwargs)

    def _weight_expr(self, t, w_plus, z, v):
        return sum(cvx.abs(z[:-1])) <= self.max_fraction


class IndexRebalOpt(cp.SinglePeriodOpt):
    """Alpha with index tracking optimization policy.

    "Use Markowitz optimization to build a portfolio, maximize future return and minimize risk"
    """

    def __init__(self, alpha: cp.ReturnsForecast, costs: list, index_weights: pd.DataFrame,
                 tracking_error: float = 0.03, turnover_limit: float = 0.15):
        """

        :param alpha: alpha forecast
        :param costs: risk, transaction cost (and finance cost if necessary)
        :param tracking_error: "each components weight should deviate from CSI300 weight less than 3%"
        :param turnover_limit: "turnover rate should be less than 15%"
        """
        max_weight_const = cp.MaxWeights((index_weights + tracking_error) * (index_weights > 0))
        min_weight_const = cp.MinWeights((index_weights - tracking_error) * (index_weights > 0))
        TurnoverLimit(turnover_limit)
        constraints = [cp.LongOnly(), max_weight_const, min_weight_const]
        super(IndexRebalOpt, self).__init__(alpha, costs, constraints)
