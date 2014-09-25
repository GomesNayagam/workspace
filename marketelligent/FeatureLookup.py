# -*- coding: utf-8 -*-
import re

class BaseFeatureLookup:
    

    def GetCompiledRe(self, filename):
        
        try:

            file1 = open(filename, "r")
            restr = file1.read()
            
            result = re.compile(restr,flags=re.UNICODE|re.M|re.I|re.S)
            
            file1.close()
                        
        except Exception, e:
            if file1:
                file1.close()
            print "Error occured while parsing file for reg ex, details : " + e
               
        return result
    
    def StoreFailedLookup(self, filename, nounlist):
        
            try:

                file1 = open(filename, "w")
                
                file1.write(nounlist)
               
                file1.close()
                        
            except Exception, e:
                if file1:
                    file1.close()
                print "Error occured while writing content to the file , details : " + e
