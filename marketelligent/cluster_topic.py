import sys
import json
sys.path.append("../")

from  customcorpus import CorpusReader

import topic_classifier.topic_classifier_service as ts
from scipy.spatial import distance
import numpy as np

 



def main():
    
    docs = CorpusReader.getAllText("../customcorpus/")
    
    text_dicts = []
    
    id = 0
    for key in docs.keys():
        title_id = 1
        for text in docs[key]:
            text_dicts.append({'id': id,
                                        'title':key + "-" + text['title'],
                                        'text': text['text'],
                                        'vector': ts.vectorize(text['text'])})
            title_id += 1
            id += 1
    
    final_dicts = []
    
    links = []
    
    while len(text_dicts) != 0:
            cur_dict = text_dicts.pop(0)
            for x in text_dicts:
                links.append({'source': cur_dict['id'],
                                        'target': x['id'],
                                        'distance':  distance.euclidean(cur_dict['vector'], x['vector']) })
                                        
            del cur_dict['text']
            del cur_dict['vector']
            final_dicts.append(cur_dict)

    output = {'nodes':final_dicts,
                    'links': links}
    write_file = open("output.json", 'w')
    write_file.write(json.dumps(output, sort_keys=True,indent=4))
    
main()