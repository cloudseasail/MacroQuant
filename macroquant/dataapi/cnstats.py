from cnstats.stats import stats
import polars as pl

industry_profit_zbcode = [
    (200101, 'A020L0F'),
    (200301, 'A020M0F'),
    (201201, 'A020N0K'),
    (201801, 'A020O0K'),
]

def cnstats_industry_profit(datestr, regcode=None):
    if int(datestr) < industry_profit_zbcode[0][0]:
        print(f'cnstats_industry_profit: no data available before {industry_profit_zbcode[0][0]}')
        return pl.DataFrame()
    for date, zbcode in industry_profit_zbcode[::-1]:
        if int(datestr) >= date:
            break
    data = stats(zbcode=zbcode, datestr=datestr, regcode=regcode)
    df = pl.DataFrame()
    for d in data:
        if d[2] != datestr:
            continue
        # remove total
        if d[1][-2:] == '01':
            continue
        if d[0].endswith('利润总额_累计值'):
            df = df.vstack(pl.DataFrame({
                'industry': d[0].replace('利润总额_累计值', ''),   # 单位：亿元
                '利润总额': float(d[3]),
            }))
    return df


def cnstats_industry_employment(datestr, regcode=None):
    if int(datestr) < 202001:
        print(f'cnstats_industry_employment: no data available before 202001')
        return pl.DataFrame()
    zbcode = 'A020O0Q'
    data = stats(zbcode=zbcode, datestr=datestr, regcode=regcode)
    df = pl.DataFrame()
    for d in data:
        if d[2] != datestr:
            continue
        # remove total
        if d[1][-2:] == '01':
            continue
        if d[0].endswith('平均用工人数_累计值'):
            df = df.vstack(pl.DataFrame({
                'industry': d[0].replace('平均用工人数_累计值', ''), 
                '平均用工人数': float(d[3])*10000,  # 单位：万人
            }))
    return df
