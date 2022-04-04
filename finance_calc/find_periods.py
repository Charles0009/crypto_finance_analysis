

from cmath import nan
from turtle import shape, st
from warnings import catch_warnings
import pandas as pd
import numpy as np
import mplfinance
from mplfinance.original_flavor import candlestick_ohlc
import yfinance
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import os
import sys
import time
import datetime

# Insert the path of modules folder
sys.path.insert(0, str(os.getcwd())+'/apis/')

from get_data_api_b import get_pd_daily_histo_between_dates
from get_data_api_b import get_pd_weekly_histo_between_dates
from get_data_api_b import get_pd_3_days_histo_between_dates

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


def cut_period_into_trends(pair, start_date, end_date, time_sensivity_in_days=0, ranging='day'):

    if type(start_date) == int:
        start_text = pd.to_datetime(start_date, unit='s')
        start_text = start_text.strftime("%d %b %Y")
        end_text = pd.to_datetime(end_date, unit='s')
        end_text = end_text.strftime("%d %b %Y")

        if ranging == 'day':
            df = get_pd_daily_histo_between_dates(pair, start_text, end_text)
        elif ranging == 'week':
            df = get_pd_weekly_histo_between_dates(pair, start_text, end_text)
        elif ranging == '3days':
            df = get_pd_3_days_histo_between_dates(pair, start_text, end_text)

    else:
        if ranging == 'day':
            df = get_pd_daily_histo_between_dates(pair, start_date, end_date)
        elif ranging == 'week':
            df = get_pd_weekly_histo_between_dates(pair, start_date, end_date)
        elif ranging == '3days':
            df = get_pd_3_days_histo_between_dates(pair, start_date, end_date)

    df.rename(columns={'Open_Time': 'Date'}, inplace=True)

    # name = 'SPY'
    # ticker = yfinance.Ticker(name)
    # df = ticker.history(interval="1d", start="2021-03-15", end="2021-07-15")
    # df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    def isSupport(df, i):
        # and df['Low'][i+1] <= df['Low'][i +2] and df['Low'][i-1] <= df['Low'][i-2] # and df['Low'][i+2] < df['Low'][i+3] and df['Low'][i-2] < df['Low'][i-3]
        support = df['Low'][i] <= df['Low'][i -
                                            1] and df['Low'][i] <= df['Low'][i+1]
        return support

    def isResistance(df, i):
        # and df['High'][i+1] >= df['High'][i +2] and df['High'][i-1] >= df['High'][i-2] # and df['High'][i+2] > df['High'][i+3] and df['High'][i-2] > df['High'][i-3]
        resistance = df['High'][i] >= df['High'][i -
                                                 1] and df['High'][i] >= df['High'][i+1]
        return resistance

    # print(df)

    levels = []

    for m in range(2, df.shape[0]-2):
        index = df.shape[0] - (m+1)
        # print(index, isSupport(df, index),isResistance(df, index), df['Low'][index], df['High'][index], df['Low'][index+1], df['High'][index+1], df['Low'][index+2], df['High'][index+2]   )

        if isSupport(df, index):
            levels.append((index, df['Low'][index],
                          df['Date'][index], "support"))
        elif isResistance(df, index):
            levels.append((index, df['High'][index],
                          df['Date'][index], "resistance"))

    for i in range(2, df.shape[0]-2):
        if isSupport(df, i):
            levels.append((i, df['Low'][i], df['Date'][i], "support"))
        elif isResistance(df, i):
            levels.append((i, df['High'][i], df['Date'][i], "resistance"))

    df['swings'] = np.nan
    df['SuppResi'] = np.nan

    # print(levels)

    df_pivots = pd.DataFrame()
    i = 0
    pd.options.mode.chained_assignment = None

    g = int(len(levels)/2)
    levels = levels[:len(levels)-g or None]

    for element in levels:
        df['swings'][element[0]] = 1
        df['SuppResi'][element[0]] = element[3]
        df_pivots[i] = df.iloc[element[0]]
        i += 1

    #df['swings'][0] = 1

    df_pivots = df_pivots.T

    df_pivots = df_pivots[::-1].reset_index(drop=True)

    # df_pivots['Date'] = df_pivots['Date'].apply(mpl_dates.num2date)
    # print(df.head(25))
    # print(df_pivots.head(25))

    #df['swings'][0] = 1

    final_pivots_df2 = pd.DataFrame()
    df_pivots_line2 = pd.DataFrame()
    o = 0

    # print("///////", df_pivots)

    while o < (df_pivots.shape[0]-1):

        if df_pivots['SuppResi'][o] == df_pivots['SuppResi'][o+1]:
            if df_pivots['SuppResi'][o] == 'support':
                if df_pivots['Low'][o] < df_pivots['Low'][o+1]:
                    df_pivots_line2 = pd.DataFrame(df_pivots.loc[o])
                    df_pivots_line2 = df_pivots_line2.T
                    final_pivots_df2 = pd.concat(
                        [final_pivots_df2, df_pivots_line2], ignore_index=True)

                elif df_pivots['Low'][o] > df_pivots['Low'][o+1]:
                    df_pivots_line2 = pd.DataFrame(df_pivots.loc[o+1])
                    df_pivots_line2 = df_pivots_line2.T
                    final_pivots_df2 = pd.concat(
                        [final_pivots_df2, df_pivots_line2], ignore_index=True)

            elif df_pivots['SuppResi'][o] == 'resistance':
                if df_pivots['High'][o] > df_pivots['High'][o+1]:
                    df_pivots_line2 = pd.DataFrame(df_pivots.loc[o])
                    df_pivots_line2 = df_pivots_line2.T
                    final_pivots_df2 = pd.concat(
                        [final_pivots_df2, df_pivots_line2], ignore_index=True)

                elif df_pivots['High'][o] < df_pivots['High'][o+1]:
                    df_pivots_line2 = pd.DataFrame(df_pivots.loc[o+1])
                    df_pivots_line2 = df_pivots_line2.T
                    final_pivots_df2 = pd.concat(
                        [final_pivots_df2, df_pivots_line2], ignore_index=True)

            o += 1

        elif df_pivots['SuppResi'][o] != df_pivots['SuppResi'][o+1]:
            df_pivots_line2 = pd.DataFrame(df_pivots.loc[o])
            df_pivots_line2 = df_pivots_line2.T
            final_pivots_df2 = pd.concat(
                [final_pivots_df2, df_pivots_line2], ignore_index=True)

        o += 1


    if (final_pivots_df2.tail(1)['SuppResi'].values) != (df_pivots.tail(1)['SuppResi'].values):
        final_pivots_df2 = pd.concat(
            [final_pivots_df2, pd.DataFrame(df_pivots.tail(1))], ignore_index=True)

    end_value_type = final_pivots_df2.tail(1)['SuppResi'].values
    beg_value_type = final_pivots_df2.head(1)['SuppResi'].values

    if end_value_type == 'resistance':
        end_value_price = final_pivots_df2.tail(1)['High'].values
    else:
        end_value_price = final_pivots_df2.tail(1)['Low'].values

    if beg_value_type == 'resistance':
        beg_value_price = final_pivots_df2.head(1)['High'].values
    else:
        beg_value_price = final_pivots_df2.head(1)['Low'].values



    liste_dates2 = []

    # final_pivots_df2['Date'] = final_pivots_df2['Date'].apply(mpl_dates.date2num)

    for q in range(0, final_pivots_df2.shape[0]):
        try:
            # if (final_pivots_df2['Date'][q+2] + final_pivots_df2['Date'][q]) >= time_sensivity_in_days :
            liste_dates2.append(final_pivots_df2['Date'][q])
        except:
            pass

    s = 0

    for u in range(0, df.shape[0]):
        if df['swings'][u] == 1:
            df['swings'][u] = np.nan

        if df['Date'][u] in liste_dates2:
            df['swings'][u] = 1

        if np.isnan(df['swings'][u]):
            df['SuppResi'][u] = np.nan


    df['swings'][df.shape[0]-1] = 1
    df['swings'][0] = 1



    if df['Open'][0] < beg_value_price :  
        df['SuppResi'][0] = 'support'
    else:
        df['SuppResi'][0] = 'resistance'

    if df['Open'][df.shape[0]-1] < end_value_price :  
        df['SuppResi'][df.shape[0]-1] = 'support'
    else:
        df['SuppResi'][df.shape[0]-1] = 'resistance'




    levels2 = []

    f = 0
    s = 0 
    value_type2 = ''
    value_type1 = 'ras'

    for x in range(0, df.shape[0]):
        
        if x == (df.shape[0] -1) :
            f =1

        if df["swings"][x] == 1:
            
            value_type1 = df["SuppResi"][x]
            if df["SuppResi"][x] == 'resistance':
                if f == 1 and value_type1 == value_type2 : 
                    levels2 = levels2[:-1]
                levels2.append(
                    (x, df['High'][x], df['Date'][x], df["SuppResi"][x]))
            if df["SuppResi"][x] == 'support':
                if f == 1 and value_type1 == value_type2 : 
                    levels2 = levels2[:-1]
                levels2.append(
                    (x, df['Low'][x], df['Date'][x], df["SuppResi"][x]))
            s+=1
            if s == 2 and value_type1 == value_type2 : 
                levels2 = levels2[:-1]
            value_type2 = value_type1
    
    
    df2 = df.copy()

    df2['Date'] = df2['Date'].apply(mpl_dates.num2date)

    result_liste = []
    f = 0
    s = 0 
    value_type2 = ''
    value_type1 = 'ras'

    for x in range(0, df.shape[0]):
        if x == (df.shape[0] -1) :
            f =1
        df2['Date'][x] = time.mktime(df2['Date'][x].timetuple())

        if df["swings"][x] == 1:
            value_type1 = df["SuppResi"][x]

            if df2["SuppResi"][x] == 'resistance':
                if f == 1 and value_type1 == value_type2 : 
                        result_liste = result_liste[:-1]
                result_liste.append(
                    (x, df2['High'][x], (df2['Date'][x]), df2["SuppResi"][x]))
            if df2["SuppResi"][x] == 'support':
                if f == 1 and value_type1 == value_type2 : 
                        result_liste = result_liste[:-1]
                result_liste.append(
                    (x, df2['Low'][x], (df2['Date'][x]), df2["SuppResi"][x]))
            s+=1
            if s == 2 and value_type1 == value_type2 : 
                result_liste = result_liste[:-1]
            value_type2 = value_type1
    
    #print(df)



    ##############################################################################

    # count = 1
    # list_rows_sup = []
    # list_rows_res = []

    # for z in range(0,2):
    #     count = 1
    #     for n in range(0, df.shape[0]):
    #         if(df['swings'][n] == 1):
    #             list_rows_sup = []
    #             list_rows_res = []

    #             if(df['SuppResi'][n] == 'support'):
    #                 for l in range(0, count):
    #                     list_rows_sup.append((df['Date'][n-l], df['High'][n-l]))
    #                 max_value = max(list_rows_sup, key=lambda item: item[1])
    #                 df.loc[df['Date'] == max_value[0], ['swings']] = 1
    #                 df.loc[df['Date'] == max_value[0], ['SuppResi']] = 'resistance'

    #             elif(df['SuppResi'][n] == 'resistance'):
    #                 for p in range(0, count):
    #                     list_rows_res.append((df['Date'][n-p], df['Low'][n-p]))
    #                 print(list_rows_res)
    #                 min_value = min(list_rows_res, key=lambda item: item[1])
    #                 df.loc[df['Date'] == min_value[0], ['swings']] = 1
    #                 df.loc[df['Date'] == min_value[0], ['SuppResi']] = 'support'
    #             else:
    #                 pass
    #             # print(count)
    #             count = 1
    #         else:
    #             count = count + 1

    # levels2 = []

    # for x in range(0, df.shape[0]):
    #     if df["swings"][x] == 1:
    #         if df["SuppResi"][x] == 'resistance':
    #             levels2.append((x, df['High'][x], df['Date'][x]))
    #         if df["SuppResi"][x] == 'support':
    #             levels2.append((x, df['Low'][x], df['Date'][x]))

    # df_pivots2 = pd.DataFrame()
    # m = 0
    # for element2 in levels2:
    #     df_pivots2[m] = df.iloc[element2[0]]
    #     m += 1

    # #df['swings'][0] = 1

    # df_pivots2 = df_pivots2.T

    # df_pivots2['Date'] = df_pivots2['Date'].apply(mpl_dates.num2date)

    # # print(df_pivots2.head(37))

    # final_pivots_df = pd.DataFrame()
    # df_pivots_line = pd.DataFrame()
    # o = 0

    # while o < (df_pivots2.shape[0]-1):

    #     if df_pivots2['SuppResi'][o] == df_pivots2['SuppResi'][o+1]:
    #         df_pivots_line = pd.DataFrame(df_pivots2.loc[o])
    #         df_pivots_line = df_pivots_line.T
    #         final_pivots_df = pd.concat(
    #             [final_pivots_df, df_pivots_line], ignore_index=True)
    #         o += 1

    #     elif df_pivots2['SuppResi'][o] != df_pivots2['SuppResi'][o+1]:
    #         df_pivots_line = pd.DataFrame(df_pivots2.loc[o])
    #         df_pivots_line = df_pivots_line.T
    #         final_pivots_df = pd.concat(
    #             [final_pivots_df, df_pivots_line], ignore_index=True)
    #         o += 1

    #     o += 1

    # print("Went from " + str(df_pivots.shape[0]) + " cutpoints initially to " + str(
    #     final_pivots_df.shape[0]) + "!")

    # liste_dates = []

    # final_pivots_df['Date'] = final_pivots_df['Date'].apply(mpl_dates.date2num)

    # for q in range(0, final_pivots_df.shape[0]):
    #     try:
    #         if (final_pivots_df['Date'][q+2] - final_pivots_df['Date'][q]) >= time_sensivity_in_days:
    #             liste_dates.append(final_pivots_df['Date'][q])
    #     except:
    #         pass

    # # print(len(liste_dates))
    # # print(liste_dates)
    # # print(final_pivots_df)

    # for u in range(0, df.shape[0]):
    #     if df['swings'][u] == 1:
    #         df['swings'][u] = np.nan

    #     if df['Date'][u] in liste_dates:
    #         df['swings'][u] = 1

    #     if np.isnan(df['swings'][u]):
    #         df['SuppResi'][u] = np.nan

    # # print(df.head(50))
    # # print(df.head(50))

    # levels4 = []
    # result_liste = []

    # df2 = df.copy()

    # # print(df)
    # # print(df2)

    # df['Date'] = df['Date'].apply(mpl_dates.num2date)
    # df2['Date'] = df2['Date'].apply(mpl_dates.num2date)

    # for x in range(0, df.shape[0]):
    #     if df["SuppResi"][x] == 'resistance':
    #         levels4.append(
    #             (x, df['High'][x], (df['Date'][x]), df["SuppResi"][x]))
    #     if df["SuppResi"][x] == 'support':
    #         levels4.append(
    #             (x, df['Low'][x], (df['Date'][x]), df["SuppResi"][x]))

    # for x in range(0, df.shape[0]):
    #     df2['Date'][x] = time.mktime(df2['Date'][x].timetuple())
    #     if df2["SuppResi"][x] == 'resistance':
    #         result_liste.append(
    #             (x, df2['High'][x], (df2['Date'][x]), df2["SuppResi"][x]))
    #     if df2["SuppResi"][x] == 'support':
    #         result_liste.append(
    #             (x, df2['Low'][x], (df2['Date'][x]), df2["SuppResi"][x]))

    # df['Date'] = df['Date'].apply(mpl_dates.date2num)

    # # print(df.head(50))

    ####################################################################################################################################

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, df.values, width=0.6,
                     colorup='green', colordown='red', alpha=0.8)

    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    # for level in levels:
    #     plt.hlines(level[1], xmin=df['Date'][level[0]],
    #                xmax=max(df['Date']), colors='red')

    for levelem in levels2:

        if levelem[3] == 'resistance':
            plt.hlines(levelem[1], xmin=df['Date'][levelem[0]],
                       xmax=max(df['Date']), colors='green')
        else:
            plt.hlines(levelem[1], xmin=df['Date'][levelem[0]],
                       xmax=max(df['Date']), colors='red')

    # for levelon in levels4:

    #     if levelon[3] == 'resistance':
    #         plt.hlines(levelon[1], xmin=df['Date'][levelon[0]],
    #                    xmax=max(df['Date']), colors='green')

    #     else:
    #         plt.hlines(levelon[1], xmin=df['Date'][levelon[0]],
    #                    xmax=max(df['Date']), colors='red')

    fig.savefig('figure1.png')

    

    return (result_liste)

    ##################################  PLOT ##############################################


# liste_periods = cut_period_into_trends("BTCUSDT", "2021-10-16", "2022-02-13", 0, '3days')


# print(liste_periods)

# t = l = p = n = count =0

# for n in range(0, df.shape[0]):

#     t = df.shape[0] - n -1
#     if(df['swings'][t]==1):
#         list_rows_sup = []
#         list_rows_res = []

#         if(df['SuppResi'][t] == 'support'):
#             for l in range (0, count):
#                 list_rows_sup.append((df['Date'][t+l], df['High'][t+l]))
#             try:
#                 max_value = max(list_rows_sup,key=lambda item:item[1])
#             except:
#                 pass

#             df.loc[df['Date'] == max_value[0], ['swings']] = 1
#             df.loc[df['Date'] == max_value[0], ['SuppResi']] = 'resistance'

#         elif(df['SuppResi'][t] == 'resistance'):
#             for p in range (0, count):
#                 list_rows_res.append((df['Date'][t+p], df['Low'][t+p]))
#             try:
#                 min_value = min(list_rows_res,key=lambda item:item[1])
#             except :
#                 pass

#             df.loc[df['Date'] == min_value[0], ['swings']] = 1
#             df.loc[df['Date'] == min_value[0], ['SuppResi']] = 'support'
#         else:
#             pass
#         #print(count)
#         count = 0

#     else :
#         count = count + 1

# levels3 = []

# for x in range(0, df.shape[0]):
#     if df["swings"][x] == 1:
#         if df["SuppResi"][x] == 'resistance':
#             levels3.append((x, df['High'][x], df['Date'][x]))
#         if df["SuppResi"][x] == 'support':
#             levels3.append((x, df['Low'][x], df['Date'][x]))

# df_pivots3 = pd.DataFrame()
# m = 0
# for element3 in levels3:
#     df_pivots3[m] = df.iloc[element3[0]]
#     m += 1

# #df['swings'][0] = 1

# df_pivots3 = df_pivots3.T

# df_pivots3['Date'] = df_pivots3['Date'].apply(mpl_dates.num2date)

# final_pivots_df2 = pd.DataFrame()
# df_pivots_line2 = pd.DataFrame()
# o = 0

# while o < (df_pivots3.shape[0]-1):

#     if df_pivots3['SuppResi'][o] ==  df_pivots3['SuppResi'][o+1]:
#         if df_pivots3['SuppResi'][o] == 'support':
#             if df_pivots3['Low'][o] < df_pivots3['Low'][o+1]:
#                 df_pivots_line2 = pd.DataFrame(df_pivots3.loc[o])
#                 df_pivots_line2 = df_pivots_line2.T
#                 final_pivots_df2 = pd.concat([final_pivots_df2,df_pivots_line2], ignore_index=True)

#             elif df_pivots3['Low'][o] > df_pivots3['Low'][o+1]:
#                 df_pivots_line2 = pd.DataFrame(df_pivots3.loc[o+1])
#                 df_pivots_line2 = df_pivots_line2.T
#                 final_pivots_df2 = pd.concat([final_pivots_df2,df_pivots_line2], ignore_index=True)

#         elif df_pivots3['SuppResi'][o]== 'resistance':
#             if df_pivots3['High'][o] > df_pivots3['High'][o+1]:
#                 df_pivots_line2 = pd.DataFrame(df_pivots3.loc[o])
#                 df_pivots_line2 = df_pivots_line2.T
#                 final_pivots_df2 = pd.concat([final_pivots_df2,df_pivots_line2], ignore_index=True)

#             elif df_pivots3['High'][o] < df_pivots3['High'][o+1]:
#                 df_pivots_line2 = pd.DataFrame(df_pivots3.loc[o+1])
#                 df_pivots_line2 = df_pivots_line2.T
#                 final_pivots_df2 = pd.concat([final_pivots_df2,df_pivots_line2], ignore_index=True)

#         o+=1

#     elif df_pivots3['SuppResi'][o] !=  df_pivots3['SuppResi'][o+1]:
#         df_pivots_line2 = pd.DataFrame(df_pivots3.loc[o])
#         df_pivots_line2 = df_pivots_line2.T
#         final_pivots_df2 = pd.concat([final_pivots_df2,df_pivots_line2], ignore_index=True)

#     o+=1

# # print(final_pivots_df2)

# liste_dates2 = []

# final_pivots_df2['Date'] = final_pivots_df2['Date'].apply(mpl_dates.date2num)

# for q in range(0, final_pivots_df2.shape[0]):

#     try:
#         if (final_pivots_df2['Date'][q+2] - final_pivots_df2['Date'][q]) >= time_sensivity_in_days :
#             liste_dates2.append(final_pivots_df2['Date'][q])
#     except :
#         pass

# for u in range(0, df.shape[0]):
#     if df['swings'][u] == 1 :
#         df['swings'][u] = np.nan

#     if df['Date'][u] in liste_dates2:
#         df['swings'][u] = 1

#     if np.isnan(df['swings'][u]) :
#         df['SuppResi'][u] = np.nan
