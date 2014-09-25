import pandas as pd
import json
from collections import defaultdict


text = pd.read_csv("data/completeTaggedData.csv", sep="\t")
#text = pd.read_csv("data/ACQdata.csv", sep="\t")
sentences = text["Sentence"]
tags = text["Tag"]
tLen = len(text)

'''
#CODE TO TAG AND WRITE THE SENTENCES IN A CSV FILE
for i in range(0, tLen):
    pass

entities = open("entities.json").read()
entities = json.loads(entities)
entities = entities["data"]


new_sents = []
count = 0
for s in sentences:
    count += 1
    print count
    sent = s.decode('utf-8').encode('utf-8')
    for x in entities:
        if x[1] == "ORGANIZATION":
            ent = x[0].encode('utf-8')
            tag = x[1].encode('utf-8')
            sent = sent.replace(ent, "<"+tag[:3]+">")
    for x in entities:
        if x[1] == "LOCATION":
            ent = x[0].encode('utf-8')
            tag = x[1].encode('utf-8')
            sent = sent.replace(ent, "<"+tag[:3]+">")
    for x in entities:
        if x[1] == "PERSON":
            ent = x[0].encode('utf-8')
            tag = x[1].encode('utf-8')
            sent = sent.replace(ent, "<"+tag[:3]+">")
    new_sents.append(sent)

df1 = pd.DataFrame({'Sentence': sentences, 'Tag': tags, 'TaggedSentence': new_sents})

df1.to_csv('data/taggedSampleData.csv', sep='\t', index=False, cols=['Sentence', 'Tag', 'TaggedSentence'])'''

complete_data = []

checkthis = defaultdict(lambda: 0)
for i in range(0, tLen):
    tg = tags[i]
    sent = sentences[i]
    #if tg[0] == "N" and tg[:2] != "NC":
    #    tg = "NONE"
    '''else:
        tg = "FOUND"'''
    '''if tg in ["JOB"]:
        tg = "NACQ"'''
    if tg not in ["ACQ", "NACQ"]:
        continue
    if checkthis[tg] > 400:
        continue
    checkthis[tg] += 1
    if len(sent.split()) > 70:
        continue
    complete_data.append([tg, sent])

print checkthis
eventDict = {"ACQ":0,
             "NACQ": 1}
'''eventDict = {"NONE": 0,
             "ACQ": 1,
             "VNSP": 2,
             "JOB": 3,
             "NC": 4}'''

'''eventDict = {"ACQ": 0,
             "VNSP": 1} 


,
             "JOB": 2,
             "NC": 3,
             "NACQ": 4,
             "NVNSP": 5,
             "NJOB": 6,
             "NNC": 7} '''

def getTrainSet():
    return [[x[1], eventDict[x[0]]] for x in complete_data]




#testText = pd.read_csv("data/testSet3.csv", sep="\t")
testText = pd.read_csv("data/ACQdata.csv", sep="\t")
testSentences = testText["Sentence"]
testTags = testText["Tag"]
def getTestSet():
    #return [x[0] for x in test_sents]
    '''new_tags = []
    for x in testTags:
        if x != "ACQ":
            new_tags.append("NACQ")
        else:
            new_tags.append(x)'''
    return testSentences, testTags
