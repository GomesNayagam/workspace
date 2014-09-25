from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import metrics, ensemble, linear_model, svm
from numpy import log, ones, array, zeros, mean, std, repeat
import numpy as np
import scipy.sparse as sp
import re
import csv
from time import time
import read
from collections import defaultdict

# - Line 197 specifies a random forest model with 4 threads (2.5GB RAM per thread is needed). If necessary, reduce the n_jobs param.
# The RF makes a small improvement, so its commented out and probably not worth the effort.

PREDICTION_FILE = "preds.csv"                 # predictions will be written here 

########

def normalize(f):
    #Code to pre process data
    #TODO: normalize the text
    return f

def ngrams(data, labels, ntrain, mn=1, mx=1, nm=500, binary = False, donorm = False, stopwords = False, verbose = True, analyzer_char = False):
    f = data
    if donorm:
        f = normalize(f)
    
    ftrain = f[:ntrain]
    ftest  = f[ntrain:]
    y_train = labels[:ntrain]
    
    t0 = time()
    analyzer_type = 'word'
    if analyzer_char:
        analyzer_type = 'char'
        
    if binary:
        vectorizer = CountVectorizer(max_n=mx,min_n=mn,binary=True)
    elif stopwords:
        vectorizer = TfidfVectorizer(ngram_range=(mn, mx),stop_words='english',analyzer=analyzer_type,sublinear_tf=True)
    else:
        vectorizer = TfidfVectorizer(ngram_range=(mn, mx),sublinear_tf=True,analyzer=analyzer_type)

    if verbose:
        print "extracting ngrams... where n is [%d,%d]" % (mn,mx)
    
    X_train = vectorizer.fit_transform(ftrain)
    X_test = vectorizer.transform(ftest)
    
    if verbose:
        print "done in %fs" % (time() - t0), X_train.shape, X_test.shape

    y = array(y_train)    
    
    numFts = nm
    if numFts < X_train.shape[1]:
        t0 = time()
        ch2 = SelectKBest(chi2, k=numFts)
        X_train = ch2.fit_transform(X_train, y)
        X_test = ch2.transform(X_test)
        assert sp.issparse(X_train)        

    if verbose:
        print "Extracting best features by a chi-squared test.. ", X_train.shape, X_test.shape    
    return X_train, y, X_test
      

def run(verbose = True):
    t0 = time()

    train = read.getTrainSet()
    labels  = array([x[1] for x in train])
    train = [x[0] for x in train]

    test_data = read.getTestSet()
    
    data = train + test_data
    n = len(data)
    ntrain = len(train)


    # The number of ngrams to select was optimized by CV
    X_train1, y_train, X_test1 = ngrams(data, labels, ntrain, 1, 1, 2000, donorm = True, verbose = verbose)
    X_train2, y_train, X_test2 = ngrams(data, labels, ntrain, 2, 2, 4000, donorm = True, verbose = verbose)
    X_train3, y_train, X_test3 = ngrams(data, labels, ntrain, 3, 3, 100,  donorm = True, verbose = verbose)    
    X_train4, y_train, X_test4 = ngrams(data, labels, ntrain, 4, 4, 1000, donorm = True, verbose = verbose, analyzer_char = True)    
    X_train5, y_train, X_test5 = ngrams(data, labels, ntrain, 5, 5, 1000, donorm = True, verbose = verbose, analyzer_char = True)    
    X_train6, y_train, X_test6 = ngrams(data, labels, ntrain, 3, 3, 2000, donorm = True, verbose = verbose, analyzer_char = True)    

    X_tn = sp.hstack([X_train1, X_train2, X_train3, X_train4, X_train5, X_train6])
    X_tt = sp.hstack([X_test1,  X_test2,  X_test3, X_test4, X_test5, X_test6])
    
    if verbose:
        print "######## Total time for feature extraction: %fs" % (time() - t0), X_tn.shape, X_tt.shape
    
    predictions = runClassifiers(X_tn, labels, X_tt)
    
    print 
    print test_data
    print predictions
    print
    write_submission(predictions, PREDICTION_FILE)    
    print "Predictions written to:", PREDICTION_FILE
    
def runClassifiers(X_train, y_train, X_test, y_test = None, verbose = True):
    
    models = [  linear_model.LogisticRegression(C=3), \
                svm.SVC(C=0.3,kernel='linear',probability=True) ,  \
                #ensemble.RandomForestClassifier(n_estimators=500, n_jobs=4, max_features = 15, min_samples_split=10, random_state = 100),  \
                #ensemble.GradientBoostingClassifier(n_estimators=400, learn_rate=0.1, subsample = 0.5, min_samples_split=15, random_state = 100) \
              ]
    dense = [False, False, True, True]    # if model needs dense matrix
    
    X_train_dense = X_train.todense()
    X_test_dense  = X_test.todense()
    
    preds = defaultdict(list)
    eventDict = {"NONE": 0,
                 "ACQ": 1,
                 "VNSP": 2,
                 "JOB": 3,
                 "NC": 4}
    for ndx, model in enumerate(models):
        t0 = time()
        print "Training: ", model, 20 * '_'        
        if dense[ndx]:
            model.fit(X_train_dense, y_train)
            pred = model.predict_proba(X_test_dense)    
        else:
            model.fit(X_train, y_train)
            pred = model.predict_proba(X_test)
            print "PREDICT PROBA"
            print model.predict_proba(X_test)    
            print "PREDICT "
            print model.predict(X_test)
        print "Training time: %0.3fs" % (time() - t0)
        for x in eventDict.keys():
            preds[x].append(array(pred[:,x]))
        print array(pred[:,2])
        print array(pred[:,3])

    predictProbs = []
    for x in eventDict.keys():
        predictProbs.append(preds[x][0]*0.4 + preds[x][1]*0.6)

    predictLabels = []
    for i in range(0,len(predictProbs[0])):
        checkProb = [predictProbs[j][i] for j in range(0,len(eventDict.keys())) ]
        currentProb = max(checkProb)
        predictLabels.append([eventDict[checkProb.index(currentProb)], currentProb])
    
    final_pred = predictLabels
    
    return final_pred

def write_submission(x,filename):
    wtr = open(filename,"w")
    for i in range(len(x)):
        wtr.write(x[i][0] + "   " + str(x[i][1]))
        wtr.write("\n")
    wtr.close()
    
if __name__=="__main__":
    run()
