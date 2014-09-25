import sys
from numpy import array
import scipy.sparse as sp
import pickle
import json
from collections import defaultdict
import read_csv as read
import NERClient as ners

########

MODELS_PATH = "models/new_model2.bin"
NO_OF_MODELS = 3

########

print "Loading models"
model = pickle.load(open(MODELS_PATH, "rb"))
vectorizers = model['vectorizers']
chi_models = model['chi_models']
classifier = model['classifier']
print "DONE"
print

def normalize(f):
    #Code to pre process data
    #TODO: normalize the text
    return f

def ngrams(_id, f, donorm = False):
    if donorm:
        f = normalize(f)
    ftest  = [f]

    vectorizer = vectorizers[_id]
    X_test = vectorizer.transform(ftest)

    if chi_models:
        ch2 = chi_models[_id]
        X_test = ch2.transform(X_test)
    return X_test
      

def run(data):
    print "Input text:"
    print data

    test_ngram_data = [ngrams(i, data, donorm=True) for i in range(0, NO_OF_MODELS)]

    X_tt = sp.hstack(test_ngram_data)
    
    predictions = runClassifiers(X_tt)
    
    print "TYPE: " + str(predictions[0][0])
    print "CONFIDENCE: " + str(predictions[0][1])
    print "SCORES: " + str(predictions)
    print
    
    return json.dumps(predictions)
    
def runClassifiers(X_test):
    
    preds = defaultdict(list)
    eventDict = {0: "NONE",
                 1: "ACQ",
                 2: "VNSP",
                 3: "JOB",
                 4: "NC"}
    '''eventDict = {0: "ACQ",
                 1: "VNSP"} 
    ,
                 2: "JOB",
                 3: "NC",
                 4: "NACQ",
                 5: "NVNSP",
                 6: "NJOB",
                 7: "NNC"} '''
    for model in classifier:
        pred = model.predict_proba(X_test)
        for x in eventDict.keys():
            preds[x].append(array(pred[:,x]))
    predictProbs = []
    for x in eventDict.keys():
        predictProbs.append(preds[x][0]*0.4 + preds[x][1]*0.6)

    predictLabels = []
    for i in range(0,len(predictProbs[0])):
        checkProb = [predictProbs[j][i] for j in range(0,len(eventDict.keys())) ]
        #currentProb = max(checkProb)
        predictLabels.append([[eventDict[checkProb.index(currentProb)], currentProb] for currentProb in checkProb])

    final_pred = predictLabels[0]
    final_pred = sorted(final_pred, key=lambda x: x[1], reverse=True)

    return final_pred
    
    
def testModel(sentences, tag):
    correct = 0
    wrong = 0
    ch = defaultdict(lambda:{"correct":0,"wrong":0})
    for i in range(0,len(sentences)):
        print "Sentence " + str(i)
        data = sentences[i]
        entities = ners.get_entities(data)
        for ent in entities.keys():
            if isinstance(entities[ent], list):
                for x in entities[ent]:
                    data = data.decode('utf-8').encode('utf-8')
                    ent = ent.decode('utf-8').encode('utf-8')
                    x = x.encode('utf-8')
                    data = data.replace(x, "<" + ent.upper()[:3] + ">")
        data = data.lower()
        correct_tag = tag[i].strip()
        if correct_tag[0] == "N" and correct_tag[:2] != "NC":
            correct_tag = "NONE"

        test_ngram_data = [ngrams(j, data, donorm=True) for j in range(0, NO_OF_MODELS)]

        X_tt = sp.hstack(test_ngram_data)
        
        predictions = runClassifiers(X_tt)
        
        predicted_tag = str(predictions[0][0])
        if correct_tag != predicted_tag:
            ch[correct_tag]["wrong"] += 1
            wrong += 1
            print data
            print "CORRECT TAG: " + correct_tag
            print "PREDICTED TAG: " + predicted_tag
        else:
            ch[correct_tag]["correct"] += 1
            correct += 1
    print "TOTAL: " + str(len(sentences))
    print "CORRECT: " + str(correct)
    print "WRONG: " + str(wrong)
    print "ACCURACY: " + str(correct*100.0/len(sentences))
    print
    for k in ch.keys():
        print k
        print "TOTAL: " + str(ch[k]["correct"] + ch[k]["wrong"])
        print "CORRECT: " + str(ch[k]["correct"])
        print "WRONG: " + str(ch[k]["wrong"])
        print "ACCURACY: " + str(ch[k]["correct"]*100.0/(ch[k]["correct"] + ch[k]["wrong"]))
        print
    
if __name__=="__main__":
    tool_type = "manual"
    if len(sys.argv) > 1:
        tool_type = sys.argv[1]
    if tool_type == "test":
        testSentences, testTags = read.getTestSet()
        testModel(testSentences, testTags)
    else:
        while True:
            print "Enter sentence:"
            txt = raw_input()
            run(txt)
