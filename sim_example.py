import logging

import cvxportfolio as cp
import pandas as pd

from optimizer.alpha import MomentumAlpha
from optimizer.blp import get_index_weights, get_index_members_ret
from optimizer.opt import IndexRebalOpt
from optimizer.risk import HistCovRiskModel

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    # config
    index = 'SHSZ300 Index'  # CSI 300
    sim_start_date = pd.Timestamp(2021, 1, 1)
    sim_end_date = pd.Timestamp(2022, 9, 16)

    # load index data
    idx_weight = get_index_weights(index)
    returns = get_index_members_ret(index)
    returns['cash'] = 0

    # build alpha forecast
    alpha = MomentumAlpha(returns, 250)

    # build risk model
    gamma_risk = 0.1  # turnover rate is better controlled through gamma_risk (alpha sensitivity to risk)
    risk_model = HistCovRiskModel(returns, 250 * 5)  # "or past 5 years daily data to calculate Cov matrix"

    # build transaction cost model
    tcost_model = cp.TcostModel(half_spread=6e-4)  # CN-A market charge is around 6 bps

    # build optimizer policy
    ir_policy = IndexRebalOpt(alpha, [gamma_risk * risk_model], idx_weight)

    # build initial portfolio
    # "Suppose we initially have a basket of $10 million CSI300 underlying stocks, with equal weights."
    init_port = (idx_weight.loc[sim_start_date] > 0) * 10e6 / 300
    init_port['cash'] = 0

    # simulation
    market_sim = cp.MarketSimulator(returns, [], cash_key='cash')
    result = market_sim.run_backtest(init_port, start_time=sim_start_date, end_time=sim_end_date, policy=ir_policy)
    result.summary()

    # output
    result.v.plot(backend='plotly').write_html('output/port_value.html')
    result.returns.plot(backend='plotly').write_html('output/port_returns.html')
    result.h.to_csv('output/port_holdings.csv')
