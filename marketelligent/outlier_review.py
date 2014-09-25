import nltk
from nltk.tokenize import word_tokenize
from nltk.collocations import *
from nltk.corpus import stopwords
# from SentiSoClient import *
from collections import defaultdict

import pandas as pd

import  myutil2 as mu




stopList = stopwords.words('english')
stopList.extend([":", "\xc2\xa0" , "(", ")", ",", ".", "[", "]", "{", "}", "!", "?", "'s", "'ve", "'m", "'re","please","thanks","something","nothing","i", "can","my","someone","everything",
                 "thank","thing","x","things","etc","n","in","the", ".i","&","amp"])

lemmatize = nltk.stem.wordnet.WordNetLemmatizer().lemmatize

rows =pd.read_csv("outlier.csv", usecols = ["Sentence"] )
    
def main():
    
#     outliernn = ["window 8","xps 13"]
#     writeBIoulierfeaturedata(outliernn)
#     return
#     
    parser = nltk.RegexpParser("PRP : {<NNP>*}")
    
    
    prp_tree =[]
    all_text = []
    prp = defaultdict(lambda: 0)
    prpadj = defaultdict(lambda: 0)
    vrb = defaultdict(lambda: 0)
    prp_vrb = defaultdict(lambda: 0)
    for text in getText():
        for s in mu.normalize(text):
            words = word_tokenize(s)
            tagged =  nltk.pos_tag(words)
            prp_tree.append(parser.parse(tagged))
            words =[ lemmatize(x) for x in  words if lemmatize(x) not in stopList]
            all_text.extend(words)
            print "SENTENCE:"
            print s
            print "POS TAG:"
            print tagged
            print "ADJ:"
            prp_adjs = [x[0] for x in tagged if x[1][:2] == "JJ" and x[0] not in stopList]
            print prp_adjs
            for p in prp_adjs:
                prpadj[p.lower()] += 1
            print "NOUNS:"
            prp_nouns = [x[0] for x in tagged if x[1][:2] == "NN" and x[0] not in stopList]
            print prp_nouns
            for p in prp_nouns:
                prp[ lemmatize(p.lower())] += 1
            print "VERBS/ADJ:"
            verbs = [x[0] for x in tagged if x[1][:2] == "JJ" and x[0] not in stopList]
            print verbs
            for v in verbs:
                lv = lemmatize(v.lower())
                vrb[lv] += 1
                for p in prp_nouns:
                    prp_vrb[(p.lower(), lv)] += 1
#             print "SENTIMENT:"
#             print get_sentiment(s)
#             print "SUBJECTIVITY:"
#             print get_subjectivity(s)
#             print "DIALOG TYPE:"
#             print get_dialog_type(s)
#             print
        print 
        print "============================================================="
        print

    print "BIGRAMS:"
    resBigram = getBigrams(all_text)
    for x in resBigram:
        print x
    print
#     print "TRIGRAMS:"
#     for x in getTrigrams(all_text):
#         print x
#         #print x[0] + " " + x[1]
#     print
    print "MOST COMMON  NOUN:"
    most_prp_nouns = sorted(prp.items(),key=lambda x:x[1], reverse=True)
    most_prp_nouns = [x for x in most_prp_nouns if x[1] >= 4]
    for x in most_prp_nouns:
        print x
    print
#     print "MOST COMMON VERB:"
#     most_verb = sorted(vrb.items(), key=lambda x:x[1], reverse=True)
#     most_verb = [x for x in most_verb if x[1] >= 3]
#     for x in most_verb:
#         print x
#     print
    print "MOST COOCCURRING NOUN-ADJ PAIR:"
    most_prp_verb = sorted(prp_vrb.items(), key=lambda x:x[1], reverse=True)
    most_prp_verb = [x for x in most_prp_verb if x[1] >= 3]
    for x in most_prp_verb:
        print x

    print "Outlier Noun Feature"
    outliernn = []
    # ensure to consider tree with two node e.g. two NNP NNP
#     yy =  [ x[0][0] for y in prp_tree for x in y if type(x) is nltk.Tree and x.node == "PRP"]
    for x in resBigram:
        for y in most_prp_nouns:
            if(x[0] == y[0]):
                outliernn.append(x[0]+" "+ x[1])

    
    print "WRITE OUTLIER FEATURE DATA"
    writeBIoulierfeaturedata(outliernn)
    
    
def writeBIoulierfeaturedata(outliernn):
    gdata = []
    data2 =pd.read_csv("customer_review.csv" )
    rows = data2["Customer Verbatim"]
    
    for row in rows:
        sentences = nltk.sent_tokenize(row)
        sentences = mu.normalize(sentences)   
        for sent in sentences:
            words = word_tokenize(sent)
            for i in range(len(words)):
                for lw in outliernn:
                    lwl = word_tokenize(lw)
                    if lemmatize(words[i]) == lwl[0] and lemmatize(words[i+1]) == lwl[1] :
                        gdata.append(sent)
        
 
    data3 = pd.DataFrame(gdata, columns= ["Sentence"])
    data3.to_csv("outlierfeature.csv")





def getText():
    for desc in rows.itertuples(index=False):
        yield desc


def getTrigrams(text):
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(3)
    #return sorted(finder.nbest(bigram_measures.pmi, 10))
    return sorted(finder.score_ngrams(trigram_measures.chi_sq), key = lambda x : x[1], reverse = True)

def getBigrams(text):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(3)
    return sorted(finder.nbest(bigram_measures.pmi, 10))
    #return sorted(finder.score_ngrams(bigram_measures.raw_freq), key = lambda x : x[1], reverse = True)
    
main()
