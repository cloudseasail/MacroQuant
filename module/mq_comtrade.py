import comtradeapicall 
import os
import pandas as pd
from .common import *

COUNTRYCODE_FILE = 'COMTRADE_COUNTRIES.csv' 
CMDCODE_FILE = 'COMTRADE_CMDHS.csv' 

CN_COMTRADE_SUB_KEY_NAME = 'cn_comtrade_subscribe_key'

class MQ_COMTRADE():
    def __init__(self, key=''):
        if not key:
            self.key = load_setting()[CN_COMTRADE_SUB_KEY_NAME]
        else:     
            self.key = key
            save_setting({CN_COMTRADE_SUB_KEY_NAME:key})

        self.get_countrycode()
        self.ALLGOOOCODE = []


    def get_countrycode(self):
        filepath  = get_file_path(COUNTRYCODE_FILE)
        if filepath.exists():
            return pd.read_csv(str(filepath), index_col=[0])
        df = comtradeapicall.getReference('ais:countriesareas')
        df.to_csv(str(filepath))
        return df
    def get_cmdcode(self):
        filepath  = get_file_path(CMDCODE_FILE)
        if filepath.exists():
            return pd.read_csv(str(filepath), index_col=[0])
        df = comtradeapicall.getReference('cmd:HS')
        df.to_csv(str(filepath))
        return df
    
    def _convert_cmdCode(self, cmdArr):
        if cmdArr is not None:
            if len(cmdArr) == 0:
                cmdCode = 'TOTAL'
            else:
                cmdCode=''
                for c in cmdArr:
                    cmdCode += f'{int(c):02d},'
                cmdCode = cmdCode[:-1]
        else:
            cmdCode = None
        return cmdCode
    
    # Limitaion:  only support period <= 12 months
    def get_final(self, start, end, reporterCode, partnerCode='0', cmdArr=[], flowCode='M,X'):
        if start >= end:
            period = start
        else:
            period = ''
            p = start
            while (p <= end):
                period += f'{p},'
                year = int(p[:4])
                month = int(p[4:])
                month+=1
                if month > 12:
                    year +=1
                    month =1
                p = f"{year:04d}{month:02d}"
            period = period[:-1]

        cmdCode = self._convert_cmdCode(cmdArr)
        df = self._get_final(period, reporterCode, partnerCode, cmdCode, flowCode)
        return self.filter_columns(df)
    
    def get_final_with_years(self, years, reporterCode, partnerCode='0', cmdArr=[], flowCode='M,X', freqCode='M'):
        cmdCode = self._convert_cmdCode(cmdArr)
        data = pd.DataFrame()
        if freqCode == 'M':
            for year in years:
                period = ''
                for month in range(12):
                    p = f"{year:04d}{month+1:02d}"
                    period += f'{p},'
                period = period[:-1]
                df = self._get_final(period, reporterCode, partnerCode, cmdCode, flowCode, freqCode)
                df = self.filter_columns(df)
                data = pd.concat([data,df])
        if freqCode == 'A':
            period=''
            for c in years:
                period += f'{c},'
            period = period[:-1]
            df = self._get_final(period, reporterCode, partnerCode, cmdCode, flowCode, freqCode)
            data = self.filter_columns(df)

        return data

    
    def filter_columns(self, df, columns=['period', 'primaryValue', 'reporterCode', 'reporterISO', 'partnerCode', 'partnerISO', 'flowCode', 'flowDesc', 'cmdCode', 'cmdDesc', 'aggrLevel', 'isLeaf', 'refYear', 'refMonth']):
        return df[columns]
    
    # flowCode:  M=Import,  X=Export
    # partnerCode: 0=World
    def _get_final(self, period, reporterCode, partnerCode='0', cmdCode='TOTAL', flowCode='M,X', freqCode='M'):
        df = comtradeapicall.getFinalData(self.key, typeCode='C', freqCode=freqCode, clCode='HS', period=period,
                                    reporterCode=reporterCode, cmdCode=cmdCode, flowCode=flowCode, partnerCode=partnerCode,
                                    partner2Code=None,
                                    customsCode=None, motCode=None, maxRecords=10000, format_output='JSON',
                                    aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)
        length = len(df) if df is not None else 0 
        # print('getFinalData, ', period,  f'total length: {length}')
        return df
    