# ----------------------------------------------------------------------------------
# # Presenting Word Frequency Results
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import sys
import os
working_dir = str(os.getcwd())


print("Data Loaded")



tot_results = pd.read_csv(working_dir + '/BurnieYilmazRS19/resultsData/percent_totalsBTCUSDTCryptoCurrencies15 Oct 202101 Jan 2022.csv')

del tot_results['Unnamed: 0']

wc_results = pd.read_csv(working_dir + '/BurnieYilmazRS19/resultsData/wilcoxon_rankBTCUSDTCryptoCurrencies15 Oct 202101 Jan 2022.csv')

del wc_results['Unnamed: 0']

pvalue_cutoff = (0.01/3900)

print("Which words were signficant across the shifts?")


for k in range(0, tot_results.shape[1]-3):
    name_for_column = 'tot_p'+str(k)
    
    popular_token_2 = set(tot_results[tot_results[name_for_column] > 1].token.tolist())

print(popular_token_2)
liste_tokens = []

for g in range(0, tot_results.shape[1]-3):
    name_for_thing = 'p'+str(g)+'_p'+str(g+1)+'_tokens'
    name_for_column_1 = 'wc_p'+ str(g)+'_p'+str(g+1)

    result1 = set(wc_results[wc_results[name_for_column_1] < pvalue_cutoff][["token"]].token.tolist())

    liste_tokens.append((name_for_thing, result1))

print(result1)

tokens_w_filter = p1_p2_tokens & p2_p3_tokens & popular_token_2

print(tokens_w_filter)

p1_p2_rise = set(wc_results[wc_results[f"change_p1_p2"] > 0][["token"]].token.tolist())
p2_p3_rise = set(wc_results[wc_results[f"change_p2_p3"] > 0][["token"]].token.tolist())
p1_p2_fall = set(wc_results[wc_results[f"change_p1_p2"] < 0][["token"]].token.tolist())
p2_p3_fall = set(wc_results[wc_results[f"change_p2_p3"] < 0][["token"]].token.tolist())

print("Risers")

print(tokens_w_filter & p1_p2_rise & p2_p3_rise)

print("Fallers")

print(tokens_w_filter & p1_p2_fall & p2_p3_fall)

print("Price Dynamic")

print(tokens_w_filter & p1_p2_rise & p2_p3_fall)

print(tokens_w_filter & p1_p2_fall & p2_p3_rise)






    


