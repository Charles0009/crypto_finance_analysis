from __future__ import print_function

import datetime
import numpy as np 
import pandas as pd
import sklearn

from get_data_api_b import get_pd_daily_histo, test_for_oldest_possible_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
# from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
# from sklearn.qda import QDA
from sklearn.svm import LinearSVC, SVC


def create_lagged_series(symbol, start_date, lags):
    

    new_start_date = start_date -datetime.timedelta(days=365)
    date_in_string = new_start_date.strftime("%d %b %Y ") 
    ts = get_pd_daily_histo(symbol, date_in_string)
    ts = ts.set_index('Open_Time')


    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag["Today"] = ts["Close"]
    tslag["Volume"] = ts["Volume"]

    # Create the shifted lag series of prior trading period close values
    for i in range(0, lags):
        tslag["Lag%s" % str(i+1)] = ts["Close"].shift(i+1)
    
    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Volume"] = tslag["Volume"]
    tsret["Today"] = tslag["Today"].pct_change()*100.0
    

    # If any of the values of percentage returns equal zero, set them to
    # a small number (stops issues with QDA model in Scikit-Learn)
    for i,x in enumerate(tsret["Today"]):
        if (abs(x) < 0.0001):
            tsret["Today"][i] = 0.0001


    # Create the lagged percentage returns columns
    for i in range(0, lags):
        tsret["Lag%s" % str(i+1)] = \
        tslag["Lag%s" % str(i+1)].pct_change()*100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
    tsret["Direction"] = np.sign(tsret["Today"])
    tsret = tsret[tsret.index >= start_date]

    return tsret




if __name__ == "__main__":

    name = "XTZUSDT"
    oldest_value = test_for_oldest_possible_data(name)
    print(oldest_value)
    # Create a lagged series
    snpret = create_lagged_series( symbol=name, start_date = datetime.datetime(2020,9,25) , lags=5)
    #    Use the prior two days of returns as predictor
    #    values, with direction as the response
    X  = snpret[["Lag1","Lag2"]]
    y  = snpret["Direction"]

    # The test data is split into two parts: Before and after date
    start_test = datetime.datetime(2021,2,17)
    # Create training and test sets

    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    y_train = y[y.index < start_test]
    y_test = y[y.index >= start_test]
    
    # Create the (parametrised) models
    print("Hit Rates/Confusion Matrices:\n")
    models = [("LR", LogisticRegression()),
              ("LDA", LDA()),
              ("QDA", QDA()),
              ("LSVC", LinearSVC()),
              ("RSVM", SVC(
                C=1000000.0, cache_size=200, class_weight=None,
                coef0=0.0, degree=3, gamma=0.0001, kernel='rbf',
                max_iter=-1, probability=False, random_state=None,
                shrinking=True, tol=0.001, verbose=False)
               ),
               ("RF", RandomForestClassifier(
                    n_estimators=1000, criterion='gini',
                    max_depth=None, min_samples_split=2,
                    min_samples_leaf=1, max_features='auto',
                    bootstrap=True, oob_score=False, n_jobs=1,
                    random_state = None, verbose = 0)
               )]
    
    # Iterate through the models
    for m in models:
        # Train each of the models on the training set
        m[1].fit(X_train, y_train)
        # Make an array of predictions on the test set
        pred = m[1].predict(X_test)
        # Output the hit-rate and the confusion matrix for each model
        print("%s:\n%0.3f" % (m[0], m[1].score(X_test, y_test)))
        print("%s\n" % confusion_matrix(pred, y_test))