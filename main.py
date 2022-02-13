#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/11/26 10:45:57
@Author  :   Dominik Lindorfer 
@Contact :   dlindo@posteo.at
@License :   (C)Copyright
@Version :   0.3
@Descr   :   None
'''

import csv
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib as mpl

def getDemoData(df, year_prefix, range):
    
    all_demo = []

    for year in range:

        year_str = year_prefix + str(year)
        cur_demo = np.zeros(120)

        with open("OGD_" + year_str + ".csv") as csvdatei:
            csv_reader_object = csv.reader(csvdatei, delimiter=';')
            next(csvdatei, None)  # skip the header

            for row in csv_reader_object:
                row[3] = row[3].split('-')
                cur_demo[int(row[3][1])] = cur_demo[int(row[3][1])] + int(row[4])
        
        all_demo.append(cur_demo)
        df[year_str] = cur_demo

df = pd.DataFrame()

getDemoData(df, "200", range(4,10,1))
getDemoData(df, "20", range(10,22,1))

# Linear-Shift to "forecast" following 9 years
for year in range(1,20,1):
    df[str(2021 + year)] = df["2021"].shift(periods=year).fillna(0)

# Get Mortality in Range 65-100
mortality = []
for year in range(1,12,1):
    mortality.append(sum(df[str(2009 + year)][64:])-sum(df[str(2009 + year + 1)][65:]))
    # print(str(2009 + year+1), sum(df[str(2009 + year)][64:])-sum(df[str(2009 + year + 1)][65:]))

print("Mean Mortality: ", np.mean(mortality)) # ~70000

# Demography 2004 - 2040
fig, axes = plt.subplots(nrows=37, ncols=1, figsize = (10, 25), sharey=True, tight_layout=True) #, figsize=(35/2.54, 15/2.54)

for i, c in enumerate(df.columns):
    axes[i].bar(df[c].index, df[c].values, width=1, color='royalblue', edgecolor="black", linewidth=2, label = c)
    axes[i].bar(range(20,35), 200000, width=1, color='red', linewidth=2, alpha=0.45)
    axes[i].bar(range(65,100), 200000, width=1, color='green', linewidth=2, alpha=0.45)
    leg = axes[i].legend(loc='right', prop={'size': 14}, handletextpad=0, handlelength=0, markerscale=0, framealpha=1)
    for item in leg.legendHandles:
        item.set_visible(False)
    # axes[i].set_ylabel("# People", fontsize=14)
    axes[i].tick_params( direction = 'in' )
    axes[i].xaxis.tick_top()
    axes[i].set_xlabel("Age / Years", fontsize=18, labelpad=20)
    axes[i].xaxis.set_label_position('top') 
    axes[i].set_xticks(np.arange(0,125,5))
    axes[i].set_yticks([0,75000,150000])
    axes[i].grid(visible=True)
    axes[i].set_axisbelow(True)
    
for ax in axes.flat:
    ax.label_outer()

fig.supylabel('# People', fontsize=18)

fig.text(0.05, 0.9835, 'Group 25-35', fontsize=12, ha='left', va='top', transform=fig.transFigure)
rect1 = mpl.patches.Rectangle((0.07, 1.7), width=0.1, height=0.35, color="Red", alpha=0.45, transform=axes[0].transAxes, clip_on=False)
axes[0].add_patch(rect1)

fig.text(0.05, 0.9935, 'Group 65-100', fontsize=12, ha='left', va='top', transform=fig.transFigure)
rect1 = mpl.patches.Rectangle((0.07, 2.3), width=0.1, height=0.35, color="Green", alpha=0.45, transform=axes[0].transAxes, clip_on=False)
axes[0].add_patch(rect1)

plt.show()

# Demography 2021
plt.style.use('_mpl-gallery')
plt.rcParams['font.family'] = "Arial"
plt.subplots(figsize=(35/2.54, 15/2.54))
plt.title("Demography 2021", fontsize=32, pad = 35)
plt.grid(True)
plt.xlabel("Age / Years", fontsize=22)
plt.ylabel("# People", fontsize=22)
plt.tick_params(axis='both', labelsize = 22)
plt.xticks(np.arange(0,125,5))
plt.bar(df.index, df["2021"].values, width=1, color='royalblue', edgecolor="black", linewidth=2)
plt.bar(range(25,35), 150000, width=1, color='red', linewidth=2, alpha=0.45)
plt.bar(range(65,100), 150000, width=1, color='green', linewidth=2, alpha=0.45)
plt.show()

# Plot the current # of People Selling / Buying
sellers = []
buyers = []
sellers_forecast = []
buyers_forecast = []

for i, c in enumerate(df.columns):
    
    corr_year = 17  #2021 -2004 = 17
    if(i > corr_year):
        corr = 70000
        sellers_forecast.append(np.sum(df[c][65:]) - corr * (i-corr_year))
        buyers_forecast.append(np.sum(df[c][25:40]))
    else:
        sellers.append(np.sum(df[c][65:]))
        buyers.append(np.sum(df[c][25:40]))
    
df.keys()[:18]
len(df.keys())

plt.figure(num = 3, figsize=(15, 10))
plt.plot(df.keys()[:len(buyers)], buyers, color='blue', linewidth=5.0)
plt.plot(df.keys()[:len(sellers)], sellers, color='red', linewidth=5.0)
plt.plot(df.keys(), buyers + buyers_forecast, color='blue', linewidth=4.5, linestyle='dashed')
plt.plot(df.keys(), sellers + sellers_forecast, color='red', linewidth=4.5, linestyle='dashed')
plt.legend(['Buyers', 'Sellers', 'Forecast (2021-2040) Buyers', 'Forecast (2021-2040) Sellers'], fontsize=26)
plt.tick_params(axis='both', labelsize = 24)
plt.xlabel("Year", fontsize=26, labelpad=10)
plt.ylabel("# People / 100K", fontsize=26, labelpad=10)
plt.xticks(np.arange(0,40, 4))
plt.show()

# Plot the Number of PPL Selling - PPL Buying
sellers_all = sellers + sellers_forecast
buyers_all = buyers + buyers_forecast

diff_bs = []

for s, b in zip(sellers_all, buyers_all):
    diff_bs.append(s - b)

plt.figure(num = 3, figsize=(15, 7))
plt.plot(df.keys()[:len(sellers)], diff_bs[:len(sellers)], color='red', linewidth=5.0)
plt.plot(df.keys(), diff_bs, color='red', linewidth=4.5, linestyle='dashed')
plt.legend(['Seller - Buyer Difference', 'Forecast'], fontsize=26)
plt.tick_params(axis='both', labelsize = 24)
plt.xlabel("Year", fontsize=26, labelpad=10)
plt.ylabel("# People / 100K", fontsize=26, labelpad=10)
plt.xticks(np.arange(0,40, 4))
plt.annotate('Buyers Market', fontsize=26, xy=(17, 16),  xycoords='data',
            xytext=(0.2, 0.5), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left', verticalalignment='top'
            )
plt.show()

# Anzahl an neuen Gebäuden
with open("Bestand_Geb.txt") as f:
    reader = csv.reader(f, delimiter=' ')
    next(f, None)  # skip the header

    d = []
    for row in reader:
        print(row)
        d.append({'Year': row[0], 'Zuwachs': int(row[1]), 'Bestand': int(row[2])})

dfGeb = pd.DataFrame(d)

meanInc = np.mean(dfGeb["Zuwachs"])
val2020 = dfGeb['Bestand'].iloc[-1]
d = []

for i in range(20):
    d.append({'Year': str(2021 + i), 'Zuwachs': meanInc, 'Bestand': val2020 + (i+1) * meanInc})

dfGeb_tmp = pd.DataFrame(d)
dfGeb = dfGeb.append(dfGeb_tmp, ignore_index=True)

plt.figure(num = 3, figsize=(15, 6))
plt.plot(dfGeb["Year"][:16], dfGeb["Bestand"][:16], color='red', linewidth=5, linestyle='solid')
plt.plot(dfGeb["Year"], dfGeb["Bestand"], color='red', linewidth=4.5, linestyle='dashed')
plt.legend(['Bestand', 'Forecast (linear increase)'], fontsize=26)
plt.tick_params(axis='both', labelsize = 24)
plt.xlabel("Year", fontsize=26, labelpad=10)
plt.ylabel("# / 100K", fontsize=26, labelpad=10)
plt.xticks(np.arange(0,40, 5))
plt.show()




# # Plot Demo
# fig, axes = plt.subplots(nrows=37, ncols=1)

# for i, c in enumerate(df.columns):
#     cur_axis = df[c].plot(kind='bar', ax = axes[i], figsize = (10, 20)).set_xticks(np.arange(0,125,5), alpha = 1, legend=True)

# # Set Red and Green Regions
# df2 = df.copy()
# for i, c in enumerate(df.columns):
#     df2[c] = np.where((df2.index >= 25) & (df2.index <= 40), 200000, 0)
#     df2[c].plot(kind='bar', ax = axes[i], figsize = (10, 20), alpha = 0.35, color = 'Red', width = 2).set_xticks(np.arange(0,125,5))


# df3 = df.copy()
# for i, c in enumerate(df.columns):
#     df3[c] = np.where((df3.index >= 65), 200000, 0)
#     df3[c].plot(kind='bar', ax = axes[i], figsize = (10, 20), alpha = 0.35, color = 'Green', width = 2).set_xticks(np.arange(0,125,5))



# use keyword arguments
# plt.setp(lines, color='r', linewidth=2.0)
# or MATLAB style string value pairs
# plt.setp(lines, 'color', 'r', 'linewidth', 2.0)





# df3 = pd.DataFrame()
# df3["regions"] = df["2021"]
# df3["regions"] = np.where((df.index >= 25) & (df.index <= 40), 10000, 0)



# ind = np.arange(0,105,1)
# h = np.full(len(ind), 150000)
# width = 2 

# plt.bar(ind, h, width, alpha = 0.5, color = 'Red')

# _, ax = plt.subplots()
# df["2021"].plot(kind='bar', ax = ax)
# plot(ind, h, width, alpha = 0.5, color = 'Red', ax=ax)





# ax = df['2021'].plot(kind='bar', color='blue', width=.75, legend=True, alpha=0.8)
# df['2020'].plot(kind='bar', color='maroon', width=.5, alpha=1, legend=True, ax = ax)

# ax


# import pandas as pd
# from matplotlib import pyplot as plt

# df = pd.DataFrame({'a':[1,2,3,1,2,2,2], 'b':[1,1,1,3,2,2,2]})
# # df['a'].value_counts().plot(kind = 'bar')
# # df['b'].value_counts().plot(kind = 'bar')

# fig, axes1 = plt.subplots()
# ax = df['a'].value_counts().plot(kind='bar', color='blue', width=.75, legend=True, alpha=0.8)
# df['b'].value_counts().plot(kind='bar', color='maroon', width=.5, alpha=1, legend=True, ax = ax)






# xticks = ax.xaxis.get_major_ticks()
# for i,tick in enumerate(xticks):
#     if i%5 != 0:
#         tick.label1.set_visible(False)



# plt.title("")
# plt.xticks(np.arange(0,110,5))
# ax.show()











# import numpy as np
# import matplotlib.pyplot as plt

# N = 5
# menMeans = (20, 35, 30, 35, 27)
# ind = np.arange(N)    
# width = 0.55   

# plt.bar(ind, menMeans, width)
# plt.ylabel('Scores')
# plt.title('Scores by group and gender')
# # plt.xticks(ind)
# # plt.yticks(np.arange(0, 81, 10))

# plt.show()



















