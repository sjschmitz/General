
import dataretrieval.nwis as nwis
import pandas as pd
from datetime import datetime as datetime
from datetime import date
import matplotlib.pyplot as plt

site = '13246000' #North Fork at Banks, ID
today = date.today()
instant_values = []

df, md = nwis.get_iv(sites=site,start='2023-5-1',end=today,multi_index=True,wide_format=True)
df.info() #instantaneous value is column 00060, indexed at 0

len(df.index) #quantity of rows in Pandas dataframe object

flow_values = df['00060'] #00060 is the identifier for flow information within dataframe
flow_index = df.index.tolist()
flow_index = pd.to_datetime(flow_index)
flow_index = flow_index.to_pydatetime() #a list of datetime objects that correspond to flow_values objects

fig, ax = plt.subplots()
ax.plot(flow_index,flow_values)
plt.axhline(y=1500,color='r',label='Danger Zone',alpha=0.55)
plt.axhline(y=2200,color='g',label='Fun Danger Zone',alpha=0.55)
plt.margins(x=0,y=0)
xmin, xmax, ymin, ymax = plt.axis()
ax.set(ylabel='Flow (cfs)', title='North Fork Payette at Banks')
plt.fill_between(x=flow_index,y1=2200,y2=ymax,color='g',alpha=0.10)
plt.fill_between(x=flow_index,y1=1500,y2=0,color='r',alpha=0.10)

todays_flow = int(flow_values[-1]) #most recent flow value
flowstr = (r'The current flow is %s cfs!' % (todays_flow))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(.25,0.7,flowstr,fontsize='small',verticalalignment='top',transform=ax.transAxes,bbox=props)

ax.grid()
fig.autofmt_xdate()
ax.legend()
plt.show()



