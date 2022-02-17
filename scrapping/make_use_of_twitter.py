from twt_scrapp import call_for_tweeter, get_nb_followers, get_name_for_url_quotes

import pandas as pd
import numpy as np

account_to_start_with = 'parabolic_matt'
min_num_follow = 50000
max_accounts_checked = 100


list_of_accounts_to_check = list()
list_already_checked = list()
list_of_accounts_to_check.append(account_to_start_with)
account_name = str()
p=0
actually_checked = 0
not_enougth_followers = 0
accounts_couldn_t_verify_follow = 0


while p < max_accounts_checked:

    list_of_accounts_to_check = list_of_accounts_to_check
    account_name = list_of_accounts_to_check[p]
    print("this is the accoujnt name " , account_name)

    if(account_name not in list_already_checked):
        print("we_in")
        try:
            nb_follow = get_nb_followers(account_name)
        except : 
            pass
            nb_follow = min_num_follow +1
            accounts_couldn_t_verify_follow = accounts_couldn_t_verify_follow +1
            print("the api fucked up here")

        if(nb_follow > min_num_follow):

            df_twts = call_for_tweeter(account_name, 100, 100)
            if not df_twts.empty:
                list_names_quote_url = get_name_for_url_quotes(df_twts)
                list_of_accounts_to_check = list_of_accounts_to_check +list_names_quote_url
                list_of_accounts_to_check = list(set(list_of_accounts_to_check))
                #list_of_accounts_to_check = list_of_accounts_to_check.remove(account_name)
                actually_checked = actually_checked+1
        else:
            not_enougth_followers = not_enougth_followers + 1

        list_already_checked.append(account_name)


    p = p+1
        

    print("p: ", p)    
    print("axtually checked: ", actually_checked)    
    print("not enough followers: ", not_enougth_followers)    

    print("size_of_list checked: ")
    print(len(list_already_checked))
    print("list to check : ////////////////////////////////////")
    print(list_of_accounts_to_check)


print("size_of_list to check: ")
print(len(list_of_accounts_to_check))


print("list_already checked : ////////////////////////////////////")
print(list_already_checked)












