# ----------------------------------------------------------------------------------
# # Presenting Word Frequency Results
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

print("Data Loaded")

tot_results = pd.read_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/percent_totals_0412182.csv')

del tot_results['Unnamed: 0']

wc_results = pd.read_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/wilcoxon_rank_sums_0412182.csv')

del wc_results['Unnamed: 0']

pvalue_cutoff = (0.01/3900)

print("Which words were signficant across the two shifts?")

p1_p2_tokens = set(wc_results[wc_results[f"wc_p1_p2"] < pvalue_cutoff][["token"]].token.tolist())
p2_p3_tokens = set(wc_results[wc_results[f"wc_p2_p3"] < pvalue_cutoff][["token"]].token.tolist())

popular_token_2 = set(tot_results[tot_results[f"tot_p2"] > 1].token.tolist())

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






    


