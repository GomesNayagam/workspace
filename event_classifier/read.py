import json


text = open("events.json").read()
test = open("test.txt").read()


jDict = json.loads(text)

sents = jDict["data"]
#train_size = len(sents)*4/5

#train_sents = sents[:train_size]
#test_sents = sents[train_size:]

train_sents = sents
test_sents = test.split("\n")[:-1]

eventDict = {"NONE": 0,
             "ACQ": 1,
             "VNSP": 2,
             "JOB": 3,
             "NC": 4}

def getTrainSet():
    return [[x[1], eventDict[x[0]]] for x in train_sents]

def getTestSet():
    #return [x[0] for x in test_sents]
    return test_sents
