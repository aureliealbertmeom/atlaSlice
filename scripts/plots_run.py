import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md

import pandas as pd

segment_date=['2012-01-01 00:00','2012-01-01 11:00','2012-01-01 23:00','2012-01-02 23:00','2012-01-03 23:00','2012-01-04 23:00','2012-01-05 23:00','2012-01-06 23:00','2012-01-08 23:00','2012-01-10 23:00','2012-01-12 23:00','2012-01-14 23:00','2012-01-16 23:00','2012-01-20 23:00','2012-01-26 23:00','2012-02-01 23:00','2012-02-02 23:00','2012-02-03 23:00','2012-02-04 23:00','2012-02-05 23:00','2012-02-06 23:00','2012-02-07 23:00','2012-02-08 23:00','2012-02-09 23:00','2012-02-10 23:00','2012-02-11 23:00','2012-02-12 23:00','2012-02-13 23:00','2012-02-14 23:00','2012-02-15 23:00','2012-02-16 23:00','2012-02-17 23:00','2012-02-18 23:00','2012-02-19 23:00','2012-02-20 23:00','2012-02-21 23:00','2012-02-22 23:00']

dt=[10,10,10,10,10,10,10,20,20,20,20,20,40,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60]
visco=[0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05]

all_dates=np.empty((0,0))
for date in segment_date:
    all_dates=np.append(all_dates,pd.Timestamp(date))

fig = plt.figure(figsize=(30,10))
ax = fig.add_subplot(111)
plt.plot(all_dates,dt,color='darkblue', marker='.', linestyle='solid',linewidth=1, markersize=4)
plt.ylabel("time-step in seconds")
ax.set_title("Time step evolution for initialization of eORCA36.L121-EXP15",size=20,y=1.08)
plt.xticks( rotation=25 )
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)
plt.savefig('/lus/scratch/CT1/hmg2840/aalbert/TMPPLOTS/eORCA36.L121/eORCA36.L121-EXP15-10/plot_dt_eORCA36.L121-EXP15.png',bbox_inches='tight')
plt.close()

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
ax.stairs(dt,all_dates, baseline=None, color='b',label='time step')
ax2=ax.twinx()
ax2.stairs(visco,all_dates, baseline=None, color='r',label='viscosity for tracers and momentum')
ax.set_ylabel("s",color='b')
ax2.set_ylabel("m/s",color='r')
ax.tick_params(axis='y', colors='b') 
ax2.tick_params(axis='y', colors='r') 
ax.legend(loc=2)
ax2.legend(loc=1)
ax.set_title("Time step and viscosity evolution for initialization of eORCA36.L121-EXP15",size=20,y=1.08)
plt.xticks( rotation=25 )
xfmt = md.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(xfmt)
plt.savefig('/lus/scratch/CT1/hmg2840/aalbert/TMPPLOTS/eORCA36.L121/eORCA36.L121-EXP15-10/histo_dt_eORCA36.L121-EXP15.png',bbox_inches='tight')
plt.close()

