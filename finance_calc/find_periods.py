from cmath import nan
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

# Insert the path of modules folder
sys.path.insert(0, str(os.getcwd())+'/apis/')

from get_data_api_b import get_pd_daily_histo_between_dates


plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


def cut_period_into_trends(pair, start_date_epoch, end_date_epoch, time_sensivity_in_days):

    start_text = pd.to_datetime(start_date_epoch, unit='s')
    start_text = start_text.strftime("%d %b %Y") 
    end_text = pd.to_datetime(end_date_epoch, unit='s')
    end_text = end_text.strftime("%d %b %Y") 

    # df = get_pd_daily_histo_between_dates(pair, start_text, end_text)
    df = get_pd_daily_histo_between_dates('BTCUSDT', "2021-09-15", "2022-03-15")
    df.rename(columns = {'Open_Time':'Date'}, inplace = True)


    # name = 'SPY'
    # ticker = yfinance.Ticker(name)
    # df = ticker.history(interval="1d", start="2021-03-15", end="2021-07-15")
    # df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]



    def isSupport(df, i):
        support = df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i +
                                                                            1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support


    def isResistance(df, i):
        resistance = df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i +
                                                                                    1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance


    levels = []

    for i in range(2, df.shape[0]-2):
        if isSupport(df, i):
            levels.append((i, df['Low'][i], df['Date'][i], "support"))
        elif isResistance(df, i):
            levels.append((i, df['High'][i], df['Date'][i], "resistance"))

    df['swings'] = np.nan
    df['SuppResi'] = np.nan

    #print(levels)

    df_pivots = pd.DataFrame()
    i = 0
    pd.options.mode.chained_assignment = None


    for element in levels:
        df['swings'][element[0]]= 1
        df['SuppResi'][element[0]]= element[3]
        df_pivots[i] = df.iloc[element[0]]
        i += 1

    #df['swings'][0] = 1

    df_pivots = df_pivots.T

    df_pivots['Date'] = df_pivots['Date'].apply(mpl_dates.num2date)

    df_pivots['direction'] = np.nan
    #print(df.head(25))
    # print(df_pivots.head(25))

    count = 1
    list_rows_sup = []
    list_rows_res = []


    for n in range(0, df.shape[0]):
            if(df['swings'][n]==1):
                list_rows_sup = []
                list_rows_res = []

                if(df['SuppResi'][n] == 'support'):
                    for l in range (0, count):
                        list_rows_sup.append((df['Date'][n-l], df['High'][n-l]))
                    max_value = max(list_rows_sup,key=lambda item:item[1])
                    df.loc[df['Date'] == max_value[0], ['swings']] = 1
                    df.loc[df['Date'] == max_value[0], ['SuppResi']] = 'resistance'
                        
                elif(df['SuppResi'][n] == 'resistance'): 
                    for p in range (0, count):
                        list_rows_res.append((df['Date'][n-p], df['Low'][n-p]))
                    min_value = min(list_rows_res,key=lambda item:item[1])
                    df.loc[df['Date'] == min_value[0], ['swings']] = 1
                    df.loc[df['Date'] == min_value[0], ['SuppResi']] = 'support'
                else:
                    pass
                #print(count)
                count = 1

            else : 
                count = count + 1

    levels2 = []

    for x in range(0, df.shape[0]):
        if df["swings"][x] == 1:
            if df["SuppResi"][x] == 'resistance':
                levels2.append((x, df['High'][x], df['Date'][x]))
            if df["SuppResi"][x] == 'support':
                levels2.append((x, df['Low'][x], df['Date'][x]))

    df_pivots2 = pd.DataFrame()
    m = 0
    for element2 in levels2:
        df_pivots2[m] = df.iloc[element2[0]]
        m += 1

    #df['swings'][0] = 1

    df_pivots2 = df_pivots2.T

    df_pivots2['Date'] = df_pivots2['Date'].apply(mpl_dates.num2date)



    # print(df_pivots2.head(37))


    final_pivots_df = pd.DataFrame()
    df_pivots_line = pd.DataFrame()
    o = 0

    while o < (df_pivots2.shape[0]-1):
        
        if df_pivots2['SuppResi'][o] ==  df_pivots2['SuppResi'][o+1]: 
            df_pivots_line = pd.DataFrame(df_pivots2.loc[o])
            df_pivots_line = df_pivots_line.T
            final_pivots_df = pd.concat([final_pivots_df,df_pivots_line], ignore_index=True)
            o+=1


        elif df_pivots2['SuppResi'][o] !=  df_pivots2['SuppResi'][o+1]: 
            df_pivots_line = pd.DataFrame(df_pivots2.loc[o])
            df_pivots_line = df_pivots_line.T
            final_pivots_df = pd.concat([final_pivots_df,df_pivots_line], ignore_index=True)

        o+=1
    print("Went from "+ str(df_pivots.shape[0])+ " cutpoints initially to " + str(final_pivots_df.shape[0]) + "!" )



    liste_dates = []

    final_pivots_df['Date'] = final_pivots_df['Date'].apply(mpl_dates.date2num)


    for q in range(0, final_pivots_df.shape[0]):

        try:
            if (final_pivots_df['Date'][q+2] - final_pivots_df['Date'][q]) >= time_sensivity_in_days :
                liste_dates.append(final_pivots_df['Date'][q]) 
        except :
            pass
    
    print(len(liste_dates))
    print(liste_dates)

    print(final_pivots_df)

    for u in range(0, df.shape[0]):
        if df['swings'][u] == 1 :
            df['swings'][u] = np.nan


        if df['Date'][u] in liste_dates:
            df['swings'][u] = 1
        

        if np.isnan(df['swings'][u]) :
            df['SuppResi'][u] = np.nan

    levels3 = []

    for x in range(0, df.shape[0]):
        if df["SuppResi"][x] == 'resistance':
            levels3.append((x, df['High'][x], df['Date'][x],df["SuppResi"][x]))
        if df["SuppResi"][x] == 'support':
            levels3.append((x, df['Low'][x], df['Date'][x], df["SuppResi"][x]))


    #print(df.head(50))
    print(df.head(50))


    ##################################  PLOT ##############################################


    # fig, ax = plt.subplots()
    # candlestick_ohlc(ax,df.values,width=0.6, \
    #                 colorup='green', colordown='red', alpha=0.8)

    # date_format = mpl_dates.DateFormatter('%d %b %Y')
    # ax.xaxis.set_major_formatter(date_format)
    # fig.autofmt_xdate()

    # fig.tight_layout()



    # # for levelem in levels2:
    # #     plt.hlines(levelem[1],xmin=df['Date'][levelem[0]],\
    # #                 xmax=max(df['Date']),colors='red')

    # # for level in levels:
    # #     plt.hlines(level[1],xmin=df['Date'][level[0]],\
    # #                 xmax=max(df['Date']),colors='blue')

    # for levelon in levels3:

    #     if levelon[3] == 'resistance':
    #         plt.hlines(levelon[1],xmin=df['Date'][levelon[0]],\
    #                     xmax=max(df['Date']),colors='green')

    #     else:
    #         plt.hlines(levelon[1],xmin=df['Date'][levelon[0]],\
    #                     xmax=max(df['Date']),colors='red')
            

    # fig.savefig('figure1.png')

    


cut_period_into_trends("BTCUSDT", 1634403579, 1644757979, 0)





    












