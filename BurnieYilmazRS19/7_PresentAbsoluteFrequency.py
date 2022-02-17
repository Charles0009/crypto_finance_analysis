# ----------------------------------------------------------------------------------
# # Presenting Word Frequency Results
# ----------------------------------------------------------------------------------


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

print("TOTAL RESULTS")

tot_results = pd.read_csv('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/resultsData/percent_totals_long_terms_Bitcoin.csv')

tot_results.sort_values(by='tot_p1',ascending=True,kind='mergesort',inplace=True)

del tot_results['Unnamed: 0']

print("Words in at least 5\% in all stages")

consistent = tot_results[(tot_results.tot_p1 >= 5) & (tot_results.tot_p2 >= 5) & (tot_results.tot_p3 >= 5)].copy()

consistent.rename(index=str, columns={"tot_p1": "Stage 1", "tot_p2": "Stage 2", "tot_p3": "Stage 3"}, inplace=True)


print("#BITCOIN")

consistent[consistent.token == 'bitcoin'][['token','Stage 3', 'Stage 2', 'Stage 1']].plot(kind='barh',stacked=False, x='token', color=['grey', 'darkgrey', 'black'],figsize=(8,1),legend=None)

plt.xlim([45,60])

plt.xticks(np.arange(45, 57, 1.0))

plt.ylabel("")
plt.xlabel("Percentage of Submissions")
plt.tight_layout()
#plt.show()
plt.savefig('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/visuals/ConsistentTotFreqBTCLong.jpeg')
plt.close()

print("#OTHER")

consistent[consistent.token != 'bitcoin'][['token','Stage 3', 'Stage 2', 'Stage 1']].plot(kind='barh',stacked=False, x='token', color=['grey', 'darkgrey', 'black'],figsize=(10,6))

plt.axvline(x=5, color="grey", linestyle = '--')

plt.xticks(np.arange(0, 15, 1.0))

plt.ylabel("")
plt.xlabel("Percentage of Submissions")
plt.tight_layout()
#plt.show()
plt.savefig('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/visuals/ConsistentTotFreqNoBTCLong.jpeg')
plt.close()

print("Words in at least 5\% in one stage")

oneOff = pd.concat([
    tot_results[(tot_results.tot_p1 >= 5) & (tot_results.tot_p2 < 5) & (tot_results.tot_p3 < 5)],   #S1 only
    tot_results[(tot_results.tot_p1 >= 5) & (tot_results.tot_p2 >= 5) & (tot_results.tot_p3 < 5)],  #S1 and 2 only
    tot_results[(tot_results.tot_p1 >= 5) & (tot_results.tot_p2 < 5) & (tot_results.tot_p3 >= 5)],  #S1 and 3 only
    tot_results[(tot_results.tot_p1 < 5) & (tot_results.tot_p2 >= 5) & (tot_results.tot_p3 < 5)],  #S2 only
    tot_results[(tot_results.tot_p1 < 5) & (tot_results.tot_p2 >= 5) & (tot_results.tot_p3 >= 5)],  #S2 and 3 only
    tot_results[(tot_results.tot_p1 < 5) & (tot_results.tot_p2 < 5) & (tot_results.tot_p3 >= 5)]  #S3 only
], axis=0)

oneOff.rename(index=str, columns={"tot_p1": "Stage 1", "tot_p2": "Stage 2", "tot_p3": "Stage 3"}, inplace=True)

oneOff[['token','Stage 3', 'Stage 2', 'Stage 1'  ]].plot(kind='barh',stacked=False, x='token', color=['grey', 'darkgrey', 'black'],figsize=(10,8))

plt.axvline(x=5, color="grey", linestyle = '--')

plt.axhline(y=13.5, color="k", linestyle = '--',linewidth=3)
plt.text(8.5, 8, "At least 5% in Stage 1", color='k', fontweight='bold', fontsize=12)

plt.axhline(y=19.5, color="k", linestyle = '--',linewidth=3)
plt.text(8.5, 16, "At least 5% in Stage 1 and 2", color='k', fontweight='bold', fontsize=12)

plt.axhline(y=21.5, color="k", linestyle = '--',linewidth=3)
plt.text(8.5, 20, "At least 5% in Stage 2 and 3", color='k', fontweight='bold', fontsize=12)

plt.text(8.5, 22.5, "At least 5% in Stage 3", color='k', fontweight='bold', fontsize=12)

plt.xticks(np.arange(0, 15, 1.0))

plt.ylabel("")
plt.xlabel("Percentage of Submissions")
plt.tight_layout()
#plt.show()
plt.savefig('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/visuals/OneOffTotFreqLong.jpeg')
plt.close()
