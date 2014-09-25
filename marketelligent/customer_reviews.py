# -*- coding: utf-8 -*-
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.chunk.regexp import RegexpParser
from nltk.tag.util import *
from collections import defaultdict
import re
from PatternExtractor import AgeExtractor, TimeExtractor, DateExtractor
from textprocessor_client import Sentiment
from FeatureLookup import BaseFeatureLookup
from sets import Set
#from nltk.tag.stanford import POSTagger
from OpenNLPClient import OpenNLPPOSClient
import operator
import sys

import myutil as mu 



test= True

lookupre = BaseFeatureLookup()

r1 = lookupre.GetCompiledRe("dell-inspiron.txt")
r2 = lookupre.GetCompiledRe("common.txt")
r3 = lookupre.GetCompiledRe("dell-family.txt")

ageEX = AgeExtractor()
dateEX = DateExtractor()
timeEX = TimeExtractor()

failednoun = Set()

#st = POSTagger('stanford/english-bidirectional-distsim.tagger',  'stanford/stanford-postagger-3.3.1.jar') 

Otag = OpenNLPPOSClient()
    
sentiment = Sentiment()   

def gettag(sent):
        tagged =  nltk.pos_tag(word_tokenize(sent))
        #tagged = Otag.pos_tag(sent)
        return tagged

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
  
def writefailednountofile(filename, nounlist):
    lookupre.StoreFailedLookup(filename, nounlist)

def buildchunkerlist(grammerlst, tagged):
    gtree = []
    for g in grammerlst:
        chunker = RegexpParser(g)
        OP = chunker.parse(tagged)
        if (OP.height() >= 3 ):
            gtree.append(OP.subtrees(lambda t: t.height() == 2))
            
    return gtree

def isNNComboexists(st, combo):
    
    if not ("/NN" in st):
        return False
    
    for c in combo:
        if (c in st):
            return True
        
    return False
 
def ifexistsinlookup(str1, lookuplist):
    
    for item in lookuplist:
        if item.match(str1):
            return True
        
    failednoun.add(str1)
    return False

def list2str(lst):
    return ' '.join(lst)

def strinlist(str1, lst1):
    return str1 in ' '.join(lst1)
    
def features(gtree, cotag, lookuplist, nnonly=False):
    
    featuredict = defaultdict(list)
      
    for tup in gtree:
        for m in tup:
            if (  isNNComboexists(str(m), cotag) or ("/NN" in str(m) and nnonly)  ):
                for word, tag in m:
                    if(tag == "NN"):
                        if ( ifexistsinlookup(word, lookuplist) ) and (not strinlist(list2str(untag(m)), featuredict[word])):
                            featuredict[word].append(list2str(untag(m)))

    return featuredict

def parseOpinionSentence2(tagged):
    grammers = []

    grammers.append('''
    OP5: {<VBG><.*>+<NN>}
    ''')

    gtree = buildchunkerlist(grammers, tagged)
   
    cotag = ["/VBG"]
    #lookuplist = [r1,r2]
    lookuplist = [r1]
    
    return  features(gtree, cotag, lookuplist, True)
    
def parseOpinionSentence(tagged):
    
    grammers = []
    res = None

    grammers.append('''
    OP1: {<NN><NNS>?<RB>?<JJ>}
    ''')
    grammers.append('''
    OP2: {<VB.?><DT>?<NN>?<IN>?<NN>} 
    ''')
    grammers.append('''
    OP3: {<JJ><NN.?>}
    ''')
    grammers.append('''
    OP4: {<NN.?>*<VB(G|N|D|Z)?><RB>?<JJ><RB>?}
    ''')
    
    gtree = buildchunkerlist(grammers, tagged)

    cotag = ["/JJ", "/VBG", "/VBN",  "/VBD","/VB", "/VBZ"]
    #lookuplist = [r1,r2]
    lookuplist = [r1]
    if (gtree):
        res =  features(gtree, cotag, lookuplist)


#     if (not res):
#         res = parseOpinionSentence2(tagged)

    return res, gtree

def parseLoyaltyfeature(sent):
        
        loyalsent = []
        trueloyalsent = []
        
        for subsent in sent.split(","):
            if lookforlayaltyword(subsent):
                loyalsent.append(subsent)
                
        for sent in loyalsent:
            tagged = gettag(sent)
            if parseRelatedFeature(sent, tagged) == True:
                trueloyalsent.append(sent)
            
            
        return trueloyalsent    
 
def lookforlayaltyword(text):            
                    
        result = ageEX.GetMatchedList(text)
        res = ""
        found = False
        for m in result:
            res = res + m.title + ", "
            found = True
            
        if (found):
            return res
    
        result = dateEX.GetMatchedList(text)
        for m in result:
            res = res + m.title + ", "
            found = True
            
        if (found):
            return res
        
        result = timeEX.GetMatchedList(text)
        for m in result:
            if ("second" not in m.title and "minute" not in m.title and "hr" not in m.title and "today" not in m.title):
                res = res + m.title + ", "
                found = True
            
        return res


def parseRelatedFeature(sent, tagged):
    
    chunker = RegexpParser(''' OP5: {<.*>+<NN>?<CD><.*>+<NN>?} ''')
    OP = chunker.parse(tagged)
    if (OP.height() >= 3 ):
        for m in OP.subtrees(lambda t: t.height() == 2):
            for (word,tag) in m:
                if ( tag == "NN" and r3.match(word)):
                    return True

def parseforloyalty(tagged):
    
    grammers = []

    grammers.append('''
    OP1: {<VB(N|P|D)><CD>?<JJ>?<NN.?>}
    ''')

    cotag = ["/VBN","/NN","/VBP", "/VBD","/JJ"]
    lookuplist = [r3]
    gtree = buildchunkerlist(grammers, tagged)
    
    res = features(gtree, cotag, lookuplist)
    
    if (not res):
        res = parseforloyalty2(tagged)

    return res
    

def parseforloyalty2(tagged):
    
    grammers = []

    grammers.append('''
    OP1: {<JJ><NN.?>}
    ''')

    cotag = ["/JJ"]
    lookuplist = [r3]
    gtree = buildchunkerlist(grammers, tagged)
    
    res = features(gtree, cotag, lookuplist)
    
    return res

    
def getloyalty(sent):
        sent = sent.lower()
        if  [ True for w in word_tokenize(sent) if r3.match(w)]:
            tagged = gettag(sent)
            if (parseforloyalty(tagged)):
                return True
            elif (parseLoyaltyfeature(sent)):
                return True
            else:
                return False
        else:
            return None
                

        
def displaystat(sent):    
        
        sent = sent.lower()
        tagged =  gettag(sent)
        result = parseOpinionSentence(tagged)
        if (result):
            return result
        else:
            return None
#         if (result):
#             print tagged
#             print sent
#             print result
#             print "--------------------------------------------------"        
#         else:
#             print "Failed: " + sent
#             print tagged
#             print "-------------------------------------------------"
        #print "(Sentence Sentiment :  " + str( sentiment.analyzetext(sent)) + ") "+ sent


def showloyalty():

    i =0
    for row in rows:
        i+=1
        #print "row number " + str(i)
        #print "---------------------------------"
        sentences = nltk.sent_tokenize(row)
        for sent in sentences:
            if (getloyalty(sent) == True):
                print sent
                print "(Feature Sentiment : " + str( sentiment.analyzetext(sent)) + ") "
                print "-----------------------------------------------"


def polarity(mset):
    
    totalscore = 0;
    for sent in mset:
        totalscore += sentiment.analyzetext(sent)
    
    return (totalscore/len(mset))

def percentage(part, whole):
  return 100 * float(part)/float(whole)
  

def tuplelst2str(tuplst):
    str1 =""
    for t in tuplst:
        str1 += t[0]+", "

    return str1[:-2]

def transform(mdict):
    if (mdict["edge"]):
        mdict["form-factor"].update(mdict.pop("edge"))
    if (mdict["casing"]):
        mdict["form-factor"].update(mdict.pop("casing"))
        
    return mdict    

def demodisplay(totalfeature):
    print bcolors.OKBLUE + "Processing done. Preparing summary..."+ bcolors.ENDC 

    likefeature = defaultdict(int)
    
    
    for x in totalfeature.items():
        likefeature[x[0]] = polarity(x[1])

    sorted_x = sorted(likefeature.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    print
    print bcolors.HEADER +"Top 5 Liked Features: "+ bcolors.ENDC
    print  bcolors.OKGREEN + tuplelst2str(sorted_x[:5]) + bcolors.ENDC
    
    print
    print bcolors.HEADER +"Top 5 Disliked Features: "+ bcolors.ENDC
    print  bcolors.FAIL + tuplelst2str(sorted_x[-5:]) + bcolors.ENDC
    
    print 
    print bcolors.HEADER +"Feature wise opinion: "+ bcolors.ENDC
    print 
    
    
    totalfeature = transform(totalfeature)
    
    for x in totalfeature.items():
        #print bcolors.WARNING+x[0]+" - "+ ",".join(x[1]) + bcolors.ENDC
        print bcolors.WARNING+x[0]+bcolors.ENDC
        print "==========="
        for y in x[1]:
            print "\t" + y
    
    print bcolors.ENDC
    
def callapriori():
    _trans = list()
    _ratingset = set()

    i=0.0
    for rate, row in rows.itertuples(index=False):
        _localset = set()
        i+=1.0
        sys.stdout.write("Processing in progress: %d%%   \r" % (float(i)/len(rows) * 100) )
        sys.stdout.flush()
        sentences = nltk.sent_tokenize(row)   
        for sent in sentences:
            feDict = displaystat(sent)
            if (feDict):
                for x in feDict.items():
                    totalfeature[x[0]].update(set(x[1]))
                    _localset.add(x[0])
        if (_localset ):
            _localset.add(rate)
            _trans.append(_localset)
            _ratingset.add(rate)

    
    itemSet = set()
    
   
    for item in totalfeature.keys():
        itemSet.add(frozenset([item])) 
 
    for item in _ratingset:
        itemSet.add(frozenset([item]))
    
    #items, rules = ap.runApriori(itemSet, _trans, 0.02 ,0.50)
    
    #ap.printResults(items, rules)
    
def writedatatocsv():
    gdata = []
    i=0
    for rdate, rating, row in rows.itertuples(index=False):
        i+=1
        sys.stdout.write("Processing in progress: %d%%   \r" % (float(i)/len(rows) * 100) )
        sys.stdout.flush()
         
        sentences = nltk.sent_tokenize(row)
        sentences = mu.normalize(sentences)   
        for sent in sentences:
            feDict = displaystat(sent)
            if (feDict):
                for x in feDict.items():
                    #totalfeature[x[0]].update(set(x[1]))
                    for y in x[1]:
                        rdata = []
                        rdata.append(rdate)
                        rdata.append(x[0])
                        rdata.append(y)
                        rdata.append(rating)
                        gdata.append(rdata)
                        

                        

    data1 = pd.DataFrame(gdata, columns= ["RDate", "Feature","Sentence","Rating"])
    data1.to_csv("result.csv")    
    

def convertrate(lst):
    if len(lst) >= 2:
        return float(lst[0])/float(lst[1])
    else:
        return lst[0]


def writewishdata(sent, gdata):
              
    if re.search("wish|like to|desire|likely", sent):
        for w in sent.split():
            if r1.match(w):
                rdata = [i, rdate, w, sent]
                gdata.append(rdata)


def writeloyaltydata(sent, gdata):
    
    if (getloyalty(sent) == True):
        loyalty = 1
    else:
        loyalty = 0
                 
    rdata = [i, rdate, sent, str(sentiment.analyzetext(sent)), convertrate(rating.split("/")), loyalty]
    gdata.append(rdata)
         
 
def writemaindata(sent, gdata):
    
    feDict = displaystat(sent)
    
    if (feDict):
        for x in feDict.items():
            #totalfeature[x[0]].update(set(x[1]))
            for y in x[1]:
                rdata = [i, rdate, x[0], y, str(sentiment.analyzetext(sent)), convertrate(rating.split("/"))]
                gdata.append(rdata)
                
def writeoutlierdata(sent, gdata):
    
    feDict, gtresult = displaystat(sent)
    
    if (not feDict  and gtresult):
        rdata = [i, rdate, sent]
        gdata.append(rdata)
                

def writeoutlierfeaturedata(sent, gdata):
        sent = sent.lower()
        if  [ True for w in word_tokenize(sent) if "windows" in w]:
            tagged = gettag(sent)
            if (parseforloyalty(tagged)):
                return True


if test:
    

    totalfeature = defaultdict(set)
    data =pd.read_csv("customer_review.csv", usecols = ["Source Date", "Customer Verbatim","Rating"] )
    rows = data

    gdata = []
    gloyal = []
    gout = []
    gwish = []
    gmain = []
    
    i=0
    for rdate, rating, row in rows.itertuples(index=False):
        i+=1
        sys.stdout.write("Processing in progress: %d%%   \r" % (float(i)/len(rows) * 100) )
        sys.stdout.flush()
         
        sentences = nltk.sent_tokenize(row)
        sentences = mu.normalize(sentences)   
        for sent in sentences:
            #writewishdata(sent, gwish)
            #writeloyaltydata(sent, gloyal)
            #writemaindata(sent, gmain)
            writeoutlierdata(sent, gout)
 
 
 
    data1 = pd.DataFrame(gout, columns= ["Rid", "RDate", "Sentence"])
    data1.to_csv("outlier.csv")

    data2 = pd.DataFrame(gmain, columns=["Rid","RDate","Feature","Sentence","Sentiment","Rating"])
    data2.to_csv("feature.csv")
    
    data3 = pd.DataFrame(gloyal, columns=["Rid","RDate","Sentence","Sentiment","Rating","Loyalty"])
    data2.to_csv("loyalty.csv")
    
    data4 = pd.DataFrame(gwish, columns=["Rid","RDate","Feature","Sentence"])
    data2.to_csv("wish.csv")



