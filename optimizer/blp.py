import os.path
import pathlib

import pandas as pd
from xbbg import blp

INPUT_FOLDER = pathlib.Path(os.path.abspath(__file__)).parent.parent.joinpath('input')


def download_index_members(index_ticker: str, start_date: str) -> None:
    """
    download index members and its weight to input folder

    :param index_ticker: bloomberg index name
    :param start_date: start date string in YYYYMMDD format
    :return:
    """
    dates = pd.bdate_range(start_date, pd.Timestamp.now())
    df = pd.DataFrame()
    for d in dates:
        idx = blp.bds(index_ticker, 'INDX_MWEIGHT_HIST', END_DT=d.strftime('%Y%m%d'))
        idx['date'] = d
        df = pd.concat([df, idx])
    df.to_csv(INPUT_FOLDER.joinpath(index_ticker + '.csv'), index=False)


def get_index_weights(index_ticker: str) -> pd.DataFrame:
    """
    get index members from local cache, in practice this goes to database with start/end date

    :param index_ticker: bloomberg index name
    :return: index members with weights
    """
    df = pd.read_csv(INPUT_FOLDER.joinpath(index_ticker + '.csv'), parse_dates=['date'])
    df['index_member'] += ' Equity'
    df = df.pivot('date', 'index_member', 'percent_weight').fillna(0) * 1e-2
    return df


def download_hist_prices(index_ticker: str, flds: str, start_date: str) -> None:
    """
    download historical prices of equities,  in practice this goes to database with start/end date

    :param index_ticker: bloomberg index name
    :param flds: bloomberg fields
    :param start_date: start date in YYYY-MM-DD
    :return:
    """
    df_index = get_index_weights(index_ticker)
    df = blp.bdh(df_index.columns, flds, start_date, CshAdjNormal=True, CshAdjAbnormal=True, CapChg=True)
    df.droplevel(1, axis=1).to_csv(INPUT_FOLDER.joinpath(index_ticker + f' {flds}.csv'))


def get_index_members_ret(index_ticker: str) -> pd.DataFrame:
    """
    get index member prices

    :param index_ticker: bloomberg index name
    :return: historical prices of index members
    """
    df = pd.read_csv(INPUT_FOLDER.joinpath(index_ticker + f' last_price.csv'), parse_dates=True, index_col=0)
    df = df.reindex(pd.bdate_range(df.index[0], df.index[-1])).ffill().bfill()
    df = df.pct_change().fillna(0)
    return df


if __name__ == '__main__':
    index_name = 'SHSZ300 Index'

    # download CSI 300 members and weights
    # download_index_members(index_name, start_date='20200101')
    print(get_index_weights(index_name))

    # download CSI 300 members historical prices
    download_hist_prices(index_name, 'last_price', '2016-01-01')
    # print(get_index_members_ret(index_name))
