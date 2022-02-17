# ----------------------------------------------------------------------------------
# # Presents VADER sentiment results
# ----------------------------------------------------------------------------------

import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import time
import matplotlib.dates as mdate

print("TERMS-RESTRICTED SUBMISSIONS")

VADERterms = pd.read_csv('./dataPrep/VADER/VADER.csv')
del VADERterms['Unnamed: 0']

print("ALL NEG / NEG + POS")

VADERterms['date'] = mdate.epoch2num(VADERterms['EpochDate'])

window = 90

for word in ["bitcoin", "tax", "ban", "DMS"]:

    VADERterms[f'{word}_ALLNEG'] = (VADERterms[f'{word}_NEG']).rolling(window).sum()
    VADERterms[f'{word}_ALLPOS'] = (VADERterms[f'{word}_POS']).rolling(window).sum()

    VADERterms[f'{word}_NEG_RATIO'] =  VADERterms[f'{word}_ALLNEG'] / (VADERterms[f'{word}_ALLPOS'] + VADERterms[f'{word}_ALLNEG'])
    VADERterms[f'{word}_POS_RATIO'] =  VADERterms[f'{word}_ALLPOS'] / (VADERterms[f'{word}_ALLPOS'] + VADERterms[f'{word}_ALLNEG'])


for word in ["bitcoin","tax", "ban", "DMS"]:
    _, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%b-%y"))
    ax.xaxis.set_major_locator( mdate.MonthLocator())
    plt.plot_date(VADERterms['date'], VADERterms[f'{word}_NEG_RATIO']*100, linestyle = '--', marker='', color = 'grey', label='negative')
    plt.plot_date(VADERterms['date'], VADERterms[f'{word}_POS_RATIO']*100, linestyle = '-', marker='', color = 'k', label='positive')
    plt.title("B")
    plt.xlim("30 March 2017", "03 Dec 2018")
    plt.axvline(x="16 Dec 2017", linestyle = '--', color='k')
    plt.axvline(x="29 June 2018", linestyle = '--', color='k')
    plt.axvline(x="15 Nov 2018", linestyle = '--', color='k')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'./visuals/VADER/{word}_VADER.jpeg')
    plt.close()

for word in ["bitcoin","tax", "ban", "DMS"]:
    _, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%b-%y"))
    ax.xaxis.set_major_locator( mdate.MonthLocator())
    plt.plot_date(VADERterms['date'], VADERterms[f'{word}_POS_RATIO']*100, linestyle = '-', marker='', color = 'k', label='positive')
    plt.title("C")
    plt.xlim("30 March 2017", "03 Dec 2018")
    plt.axvline(x="16 Dec 2017", linestyle = '--', color='k')
    plt.axvline(x="29 June 2018", linestyle = '--', color='k')
    plt.axvline(x="15 Nov 2018", linestyle = '--', color='k')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'./visuals/VADER/{word}_POS_VADER.jpeg')
    plt.close()

