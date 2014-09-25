# import sys

#sys.path.append("./gen_py")

from gen_py.textprocessor import TextProcessor
# from gen_py.textprocessor.ttypes import *
# from gen_py.textprocessor.constants import *
# from gen_py.textprocessor import ttypes


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Sentiment:

    def __init__(self):
    
        try:

            self.transport = TSocket.TSocket('localhost', 3001)
            self.transport = TTransport.TFramedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        
            self.client = TextProcessor.Client(self.protocol)

        except Thrift.TException, tx:
            print tx
    
        except Exception, e:
            print e

    def analyzetext(self, text):
        
        try:
                    
            self.transport.open()
        
            retVal = self.client.infer_sentimentType(text)
                               
            self.transport.close()
            
            return retVal
            
        except Thrift.TException, tx:
            print tx
    
        except Exception, e:
            print e