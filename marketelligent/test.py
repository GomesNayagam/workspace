#from nltk.tag.stanford import POSTagger
from nltk.data      import load
from nltk.corpus import  brown
from nltk.tag import  UnigramTagger
from nltk.tag.brill import SymmetricProximateTokensTemplate, ProximateTokensTemplate
from nltk.tag.brill import ProximateTagsRule, ProximateWordsRule, FastBrillTaggerTrainer


_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'

test = True


if test:
    
#     tagger = UnigramTagger(brown.tagged_sents(categories='reviews')[:500])
#     print tagger.tag("A very satisfied customer and I won't fail to recommend this product.".split())
#     
#     tagger = UnigramTagger(brown.tagged_sents(categories='reviews'))
#     print tagger.tag("A very satisfied customer and I won't fail to recommend this product.".split())
#     
    
    
    brown_train = list(brown.tagged_sents(categories='reviews')[:500])
    brown_test = list(brown.tagged_sents(categories='reviews')[500:600])
    #unigram_tagger = UnigramTagger(brown_train)
    unigram_tagger = UnigramTagger(brown_train)
#    unigram_tagger = load(_POS_TAGGER)
    
    templates = [
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
    SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
    SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
    ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
    ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
    ]
    
    trainer = FastBrillTaggerTrainer(initial_tagger=unigram_tagger, templates=templates, trace=3, deterministic=True)
    brill_tagger = trainer.train(brown_train, max_rules=10)
    
    #print brill_tagger.evaluate(brown_test)    

    print brill_tagger.tag("A very satisfied customer and I won't fail to recommend this product.".split())

    print "end"
    
# 
#     st = POSTagger('stanford/english-bidirectional-distsim.tagger',  'stanford/stanford-postagger-3.3.1.jar') 
#     print st.tag('What is the airspeed of an unladen swallow ?'.split()) 

    
          
  
