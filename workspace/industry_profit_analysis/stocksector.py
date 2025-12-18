
import akshare as ak
import time
import polars as pl

def get_benchmark(start_date, end_date):
    benchmark = ak.stock_zh_index_daily_em(symbol="sh000905",start_date=start_date, end_date=end_date)
    benchmark = pl.from_pandas(benchmark)
    benchmark = benchmark.with_columns(pl.col('close').pct_change().alias('bm_pct_change'))[1:]
    benchmark = benchmark.with_columns((pl.col('bm_pct_change')+1).alias('net_growth'))
    benchmark = benchmark.with_columns(pl.col('net_growth').cum_prod().alias('benchmark'))
    benchmark = benchmark.select(pl.col(['date', 'benchmark', 'bm_pct_change']))
    return benchmark

def stock_sector_net_grouwth_all(start_date, end_date):
    benchmark = get_benchmark(start_date, end_date)
    sectors = ak.stock_board_industry_name_em() 
    sectornames = list(sectors['板块名称'])
    df = benchmark.select(pl.col(['date', 'benchmark']))

    for sector_name in sectornames:
        data = ak.stock_board_industry_hist_em(symbol=sector_name, start_date=start_date, end_date=end_date, period="日k", adjust="")
        data = pl.from_pandas(data).select(pl.col(['日期', '收盘'])).rename({'日期': 'date', '收盘': 'close'})
        data = stock_sector_net_growth(data, benchmark, sector_name)
        df = df.join(data, on='date', how='inner')
        time.sleep(0.1)
    
    return df

def stock_sector_net_growth(data, benchmark, name):
    data = data.with_columns(pl.col('close').pct_change().alias('pct_change'))[1:]
    data = data.join(benchmark, on='date', how='inner')
    data = data.with_columns((pl.col('pct_change') - pl.col('bm_pct_change')).alias('net_growth'))
    data = data.with_columns((pl.col('net_growth')+1).alias('net_growth'))
    data = data.with_columns(pl.col('net_growth').cum_prod().alias(f'{name}'))
    return data.select(pl.col(['date', f'{name}']))