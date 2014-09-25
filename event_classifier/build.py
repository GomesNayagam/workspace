from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import linear_model, svm, ensemble
from numpy import array
import scipy.sparse as sp
from time import time
import read_csv as read
import pickle

########

MODELS_PATH = "models/all4.bin"

########

model = {'vectorizers': [],
         'chi_models': [],
         'classifier': None}

def normalize(f):
    f = [x.lower() for x in f]
    #Code to pre process data
    #TODO: normalize the text
    return f

def ngrams(data, labels, mn=1, mx=1, nm=500, binary = False, donorm = False, stopwords = False, verbose = True, analyzer_char = False):
    if donorm:
        data = normalize(data)
    
    ftrain = data
    y_train = labels
    
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
    model['vectorizers'].append(vectorizer)
    
    if verbose:
        print "done in %fs" % (time() - t0), X_train.shape

    y = array(y_train)    
    
    numFts = nm
    '''if numFts < X_train.shape[1]:
        t0 = time()
        ch2 = SelectKBest(chi2, k=numFts)
        X_train = ch2.fit_transform(X_train, y)
        model['chi_models'].append(ch2)
        assert sp.issparse(X_train)'''

    if verbose:
        print "Extracting best features by a chi-squared test.. ", X_train.shape    
    return X_train, y
      

def run(verbose = True):
    t0 = time()

    train = read.getTrainSet()
    labels  = array([x[1] for x in train])
    data = [x[0] for x in train]

    # The number of ngrams to select was optimized by CV
    X_train1, y_train = ngrams(data, labels, 1, 1, 2000, donorm = True, verbose = verbose)
    X_train2, y_train = ngrams(data, labels, 2, 2, 4000, donorm = True, verbose = verbose)
    X_train3, y_train = ngrams(data, labels, 3, 3, 100,  donorm = True, verbose = verbose)    
    #X_train4, y_train = ngrams(data, labels, 4, 4, 1000, donorm = True, verbose = verbose, analyzer_char = True)    
    #X_train5, y_train = ngrams(data, labels, 5, 5, 1000, donorm = True, verbose = verbose, analyzer_char = True)    
    #X_train6, y_train = ngrams(data, labels, 3, 3, 2000, donorm = True, verbose = verbose, analyzer_char = True)    

    X_tn = sp.hstack([X_train1, X_train2, X_train3])#, X_train4, X_train5, X_train6])
    
    if verbose:
        print "######## Total time for feature extraction: %fs" % (time() - t0), X_tn.shape
    
    models = runClassifiers(X_tn, labels)

    model['classifier'] = models

    pickle.dump(model, open(MODELS_PATH, "wb"))
    
    print "DONE"
    
def runClassifiers(X_train, y_train, y_test = None, verbose = True):
    
    models = [  linear_model.LogisticRegression(C=3), \
                svm.SVC(C=0.3,kernel='linear',probability=True) ,  \
                ensemble.RandomForestClassifier(n_estimators=500, n_jobs=4, max_features = 15, min_samples_split=10, random_state = 100),  \
                ensemble.GradientBoostingClassifier(n_estimators=400, subsample = 0.5, min_samples_split=15, random_state = 100) \
              ]
    dense = [False, False, True, True]    # if model needs dense matrix
    
    X_train_dense = X_train.todense()
    
    trained_models = []
    for ndx, model in enumerate(models):
        t0 = time()
        print "Training: ", model, 20 * '_'        
        if dense[ndx]:
            model.fit(X_train_dense, y_train)
        else:
            model.fit(X_train, y_train)
        print "Training time: %0.3fs" % (time() - t0)
        trained_models.append(model)

    return trained_models

    
if __name__=="__main__":
    run()
