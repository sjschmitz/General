import dataretrieval.nwis as nwis
import time as time
import pandas as pd
from datetime import datetime as datetime
from datetime import timedelta
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser as parser

NFk, MFk, SFk, MainFk = '13246000','13237920','13235000','13247500' #USGS Site ID numbers
today = datetime.now()
today = today.strftime("%Y-%m-%d")

def load_data(site_id) -> pd.DataFrame:
    global df
    format = '%Y-%m-%d'
    print('For sizing parameters, flow information will only be loaded back to 2023-04-01\n')
    err_msg = "Unable to read input dates - check spelling and format and retry"
    end = input("Input end date in YYYY-MM-DD format: ")
    res = True
    try:
        res = bool(parser.parse(end))
    except ValueError:
        print(err_msg) 
        end = input("Input end date in YYYY-MM-DD format: ")
    print('Loading Dataset...')
    df, md = nwis.get_iv(sites=site_id,start='2023-04-01',end=end,multi_index=True,wide_format=True)
    assert df.empty is False,err_msg
    df.rename(columns={'00060':'cfs'},inplace=True)
    print('Load Complete. Your Pandas Dataset is assigned to variable "df"')

#-------------------#
#Summary Statistics #
#-------------------#
err_msg = 'problem calculating function'

def year_avg(df) -> float:
    avg_unformat = df['cfs'].mean() 
    avg = "{:.2f}".format(avg_unformat)
    assert avg,err_msg
    print(f'The yearly average is {(avg)} cfs')
    return avg

def find_peak(df) -> float:
    flow_max,flow_min = df['cfs'].max(),df['cfs'].min()
    peaks = [flow_max,flow_min]
    flow_max = "{:.2f}".format(flow_max)
    flow_min = "{:.2f}".format(flow_min)
    print(f'The maximum recorded flow was {flow_max} | the minimum recorded flow was {flow_min}')
    return flow_max, flow_min

def find_peak_avg(site_id) -> list:
    """
    This function returns the flow window
    where 50% of stream peaks occur as list.
    Also returns the stream peak time over 
    the previous 10 years as key:value dictionary
    YYYY-MM-DD:CFS pair.
    """
    df, md = nwis.get_discharge_peaks(sites=site_id,start='2013-01-01',end=today,multi_index=False)
    peak_time_unf = df['peak_tm'] #datetime index of peak measurement
    peak_time_unf = peak_time_unf.index.tolist()
    peak_time_unf = pd.to_datetime(peak_time_unf)
    peak_time = peak_time_unf.strftime("%Y-%m-%d")
    peak_time_dtm = [] 
    for val in peak_time:
        peak_time_dtm.append(datetime.strptime(val,"%Y-%m-%d"))
    peak_flow = df['peak_va'] #cfs measurement of peak measurement
    peaks_final = dict(zip(peak_time, peak_flow)) #dictionary object with date:flow key-value pairs
    
    month_day = [(date.month, date.day) for date in peak_time_dtm]
    sorted_dates = [date for _, date in sorted(zip(month_day, peak_time_dtm))]
    start_index = int(len(sorted_dates) * 0.25)
    end_index = int(len(sorted_dates) * 0.75)
    avg_peak_time = sorted_dates[start_index:end_index+1] #Shows window of 50% peak times
    print(f'The average peak time is from {avg_peak_time[0].month,avg_peak_time[0].day} to {avg_peak_time[-1].month,avg_peak_time[-1].day} (MM/DD date format)')
    return avg_peak_time, peaks_final

def daily_avg(site_id):
    """
    compares 10-year average on given date
    """
    date = input('Please input date of interest in YYYY-MM-DD format: ')
    base_date = datetime(2013, 1, 1)
    end_date = datetime.strptime(date, '%Y-%m-%d')
    dfs = []
    current_year = base_date.year
    for year_offset in range(10):
        current_year += 1
        current_dte = str(f'{current_year}-{end_date.month}-{end_date.day}') 
        df, md = nwis.get_iv(sites=site_id, start=current_dte, end=current_dte)
        dfs.append(df['00060'][-1])
    print('\n')
    print(f'The following are decade-yearly averages ending with {end_date.strftime("%Y-%m-%d")}')
    print('\n' * 1)
    year_counter = 2013
    for val in dfs:
        print(f"On {year_counter}-{end_date.month}-{end_date.day}, the daily value was {int(val)}")
        time.sleep(0.5)
        year_counter += 1
    print('\n')
    print(f'The decade average for {end_date.strftime("%Y-%m-%d")} is {int(sum(dfs)/len(dfs))} cfs!')

print("Welcome to the Payette Summary Toolset!\nWritten by: Steven Schmitz")
print('\n' * 1)
print('\033[1m' + "Variable Names for Site ID's" + '\033[0m')
print("NFk : North Fork of the Payette River\nMFk : Middle Fork of the Payette River\nSFk : South Fork of the Payette River\nMainFk : Main Fork of the Payette River")
print('\n' * 1)
time.sleep(1)
def Toolset():
    print('\033[1m' + "Toolset" + '\033[0m')
    print('type Toolset() into consule to get list of functions available\n')
    print('load_data(var) : loads streamflow information from NWIS server | var = variable name for site_id')
    print('year_avg(var): returns average flow in cfs during timeframe of loaded dataset | var = pandas dataframe of loaded data; df')
    print('find_peak(var): returns peak minimum and maximum flows during timeframe of dataset | var = pandas dataframe of loaded data; df')
    print('find_peak_avg(var): returns date window where 50% of flow peaks occur | var = variable name for site_id')
    print('daily_avg(var): compares daily average of given date from 2013 to date | var = variable name for site_id')
Toolset()
