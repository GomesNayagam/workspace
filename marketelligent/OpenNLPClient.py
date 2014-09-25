import httplib2
import json
from nltk.tag.util import str2tuple

POSTAG_URL = "http://localhost:9080/tag_pos"


class OpenNLPPOSClient(object):
    
    def post_data(self, data):
        http = httplib2.Http()
        headers={'Content-Type': 'text/plain; charset=UTF-8'}

        try:

            response, content = http.request(POSTAG_URL, 'POST', headers=None, body=data)
            #yield httpclient.fetch(index_url, method='POST', postdata=data)
            if response.status < 200 or response.status > 400:
                print ("Exception occured check the status:  %s ", response.status)
            response = json.loads(content)
            return response

        except Exception as message:
            print ("Exception occured %s" %(message))
            return response


    def pos_tag(self, data):
        s =  self.post_data(data)
        if "tags" in s:
           s = s["tags"]
        else:
            return None
        return [self.transform(i) for i in s ]
        
        
    def transform(self, item):
        item = item.encode('ascii','ignore')
        return str2tuple(item, "/")


    def check_status(self):
        
        http = httplib2.Http()
                
        try:
            response  = http.request(POSTAG_URL, 'GET')
            res = response[0]
            
            if res.status == 200:
                return True
            else:
                return False

        except Exception as message:
            print ("Exception occured %s" %(message))
            return False  