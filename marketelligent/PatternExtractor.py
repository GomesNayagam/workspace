# -*- coding: utf-8 -*-
import re

class WordEntry:
    
    def __init__(self, text, startpos, endpos):
        self.title = text
        self.start = startpos
        self.end = endpos

class CurrencyExtractor:
    
    def __init__(self):
        self.regex1 = ur"(au[\$d]|cad|cny|dm|dem|eur|frf|gbp|hk[\$d]|inr|kr(w)?|nz[\$d]|rmb|rs|us[\$d]|\$|\¥|\€|\₣|\£|\₨|\₩)(\.)?\s*(((\d{1,3}[,.])+\d{3})|\d+)([,.-]\d{1,3})?(?=\s|\,\D|\b)(\s*(thousand|million|billion|trillion|m\b|k\b|b\b|bn\b|mill\.?|bill\.?))?"
        self.regex2 = ur"(((\d{1,3}[,.])+\d{3})|\d+)([,.]\d{1,3})?\s*(thousand|million|billion|trillion|m|k|b|bn|mill\.?|bill\.?)?\s*(au[\$d]|cad|cny|dm|dem|eur|frf|gbp|hk[\$d]|inr|kr(w)?|nz[\$d]|rmb|rs|sek|twd|us[\$d]|buck(s)?|cents|(us\s)?dollar(s)?|euro|frank(s)?|krona|pence|pounds|rupees|quid|shilling|yuan|yen)($|(?=([^\w]?(\b|\s|$))))"
        self.regex3 = ur"\b((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|fourty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred(\sand)?|thousand(\sand)?|million(\sand)?)\s)+(au[\$d]|cad|cny|dm|dem|eur|frf|gbp|hk[\$d]|inr|kr(w)?|nz[\$d]|rmb|rs|sek|twd|us[\$d]|buck(s)?|cents|(us\s)?dollar(s)?|euro|frank(s)?|krona|pence|pounds|rupees|quid|shilling|yuan|yen)"
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
        patterns.append(re.compile(self.regex2,flags=re.UNICODE|re.M|re.I|re.S))
        patterns.append(re.compile(self.regex3,flags=re.UNICODE|re.M|re.I|re.S))
        
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
                
        return matchedlst
    
class AgeExtractor:
    
    def __init__(self):
        self.regex1 = ur"\b((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|fourty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred(\sand)?|thousand(\sand)?|million(\sand)?)[\s-])+(year(s)?\syoung|year(s)?[\s-]old|year(s)?\sof\sage|month(s)?[\s-]old|month(s)\sof\age|day(s)?[\s-]old|birthday)\b"
        self.regex2 = ur"\b(age\sof|age|age\sis|aged|turn|turned|age:)\s((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|fourty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred(\sand)?|thousand(\sand)?|million(\sand)?)([\s-]|\b))+"
        self.regex3 = ur"\b(\d+([\/-]\d+)?)(th)?[\s-]?(birthday|yr\sold|year-old|year(s)?\sold|y\.o\.|y\.\so\.|year(s)?\sof\sage|yrs\sof\sage|years\syoung)|\b(age\sof|age|age\sis|aged|turn|turned|age:)\s+(\d+([\/-]\d+)?[\s]?(year(s)?|yrs\.|month(s)?)?)\b"
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
        patterns.append(re.compile(self.regex2,flags=re.UNICODE|re.M|re.I|re.S))
        patterns.append(re.compile(self.regex3,flags=re.UNICODE|re.M|re.I|re.S))
        
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
                
        return matchedlst

class BankAccountExtractor:
    
    def __init__(self):
        # U.S account
        self.regex1 = ur"((account|dda)([s\.]|s\.)?\s*(\#|number|no)?\s*([\:\.-])*\s*(\d(-)?(\s(?=\d))?){4,17})"
        # UK
        self.regex2 = ur"(?<=\s)(((\d\s?){6})|((\d-?){6}))(\s|-)?\d{7,10}\b"
        
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
        patterns.append(re.compile(self.regex2,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst

class SWIFTCodeExtractor:
    
    def __init__(self):
        # U.S 
        self.regex1 = ur"((([a-zA-Z](\s)?){4})?(US)([a-zA-Z0-9]{2})([a-zA-Z0-9]{1,3})?)"
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst

class CreditCardExtractor:
    
    def __init__(self):
        # U.S
        self.lstRegex = []
        
        self.lstRegex.append(ur"\b(3[47]\d{2})((([ -]?)\d{4}(\4)\d{4}(\4)\d{3}\b)|(([ -]?)\d{6}(\8)\d{5}\b))") # American express
        self.lstRegex.append(ur"\b(5610|5602)([ -]?)\d{4}(\2)\d{4}(\2)\d{4}\b") # Austral Bank card
        self.lstRegex.append(ur"\b(5019)([ -]?)\d{4}(\2)\d{4}(\2)\d{4}\b") # Dankort card
        self.lstRegex.append(ur"\b((30[0-5]\d)|(3[6-8]\d{2}))((([ -]?)\d{6}(\6)\d{4}\b)|(([ -]?)\d{4}(\9)\d{4}(\9)\d{2}\b))") # Diners Club card
        self.lstRegex.append(ur"\b(6011)([ -]?)\d{4}(\2)\d{4}(\2)\d{4}\b") # Discover card
        self.lstRegex.append(ur"\b(2014|2149)([ -]?)\d{7}(\2)\d{4}\b") # enRoute card
        self.lstRegex.append(ur"\b(35[2-8]\d|3088)([ -]?)\d{4}(\2)\d{4}(\2)\d{4}\b") # JCB card
        self.lstRegex.append(ur"\b5[1-5]\d{2}([ -]?)\d{4}(\1)\d{4}(\1)\d{4}\b") # Master card
        self.lstRegex.append(ur"\b(6334|6767)([ -]?)\d{4}(\2)\d{4}(\2)\d{4}(\2)(\d{2,3})?\b") # Solo card
        self.lstRegex.append(ur"\b((4903|4905|4911|4936|6333|6759)([ -]?)\d{4}(\3)\d{4}(\3)\d{4}(\3)(\d{1,3})?|(564182|6331([ -]?)10)\d{2}([ -]?)\d{4}([ -]?)\d{4}([ -]?)(\d{1,3})?)\b") # Switch Card
        self.lstRegex.append(ur"(\b(4\d{3})([ -]?)\d{4}(\3)\d{4}(\3)\d{4}\b)|(\b4\d{3}([ -]?)\d{4}(\7)\d{5}\b)") # Visa card
       
    def GetPatterns(self):
        patterns = []
    
        for reg in self.lstRegex:
            patterns.append(re.compile(reg,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst

class EmailExtractor:
    
    def __init__(self):
        # U.S 
        self.regex1 = ur"(?i)\b(^|(?<=[\s\(\)\{\}\[\];\.\,:\\\/\<\>]))([a-z0-9_]+(?:[a-z0-9\.!#$%&'*+/=?^_`{|}~-]+)*[@|©])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|[A-Z]{2})(?![/:])\b"
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst

class URLExtractor:
    
    def __init__(self):
        # U.S 
        self.regex1 = ur"""(?i)(^|(?<=[\s\(\)\{\}\[\];\.\,:\\\/\<\>]))(((?i)((http|https|ftp|sftp|ftps|file|ssh):(?:/{1,3}|[a-z0-9%]))([a-z0-9:@!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9:@!#$%&'*+/=?^_`{|}~-]+)*@)?)?(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|[A-Z]{2})(/(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>???“”‘’]))?(?!@)($|(?=([^\w]?(\b|\s|$)))))"""
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst

class TimeExtractor:
    
    def __init__(self):
        # U.S 
        self.regex1 = ur"(((((at|by)\s+)?([0]?[1-9]|1[0-2]|2[0-4])(h|:|\.)[0-5][0-9]((m|:|\.)[0-5][0-9][s\.:]?)?\s*([ap](\.?m\.?))\s*([GECMP][MSD]T|o'clock)?|[0-9]?[1-9]\s*(([ap]\.?m\.?)|([GECMP][MSD]T|o'clock))|([0-9]?[0-9]|1[0-2]|2[0-4])h\s?[0-5][0-9]m?(\s?[0-5][0-9][sz])?|([0-9]?[0-9]|1[0-2]|2[0-4]):[0-5][0-9]:[0-5][0-9][sz]?\s*([GECMP][MSD]T|o'clock)?)\s?((today|tomorrow|yesterday)(\s(morning|evening|afternoon))?)?)|(this|in the)\s(morning|evening|afternoon)|((last|this)\s(week|month|year))|the\sday\safter(\stomorrow)?|the\sday\sbefore(\syesterday)?|((today|tomorrow|yesterday)(\s(morning|evening|afternoon))?)|once\supon\sa\stime|(half[\s-]past|quarter[\s-]to|quarter[\s-]past)\s(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)|at\s(midnight|dawn|sunset)|(at\s)?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\so'clock|(([1-9][0-9]?)|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s?(days|weeks|months|years|yrs|hours|minutes|seconds|mins|secs)\s(ago)?|(1|one)\s?(day|week|month|year|hour|minute|second|min|sec)\s(ago)?)(\b|$)"
 
    def GetPatterns(self):
        patterns = []
    
        patterns.append(re.compile(self.regex1,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst
    
class DateExtractor:
    
    def __init__(self):
        
        self.lstRegex = []
        
        self.lstRegex.append(ur"([dD]ate.{1,4})((0?[1-9]|[12][0-9]|3[01])([.][ ]*)(0?[1-9]|1[012]))(([.][ ]*)(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\s|$|[)]))))")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))((0?[1-9]|[12][0-9]|3[01])(([-/.,][ ]*)|([ ]))(0?[1-9]|1[012]))((([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)[0-9]{2}))($|(?=([^\w]?(\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))((0?[1-9]|[12][0-9]|3[01])((([-/.,][ ]*)|([ ]+)))?(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec))(((([-/.,][ ]*)|([ ]+)))?(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))((January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)((([-/.,][ ]*)|([ ]+)))?(0?[1-9]|[12][0-9]|3[01]))((([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(([23]{0,1}1st|2?2nd|2?3rd|[12]{0,1}[4-9]th|1[123]th|[123]0th)(([-/.,][ ]*)|([ ]+))(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec))((([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))((January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)(([-/.,][ ]*)|([ ]+))([23]{0,1}1st|2?2nd|2?3rd|[12]{0,1}[4-9]th|1[123]th|[123]0th))((([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|Q1|Q2|Q3|Q4)(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|Q1|Q2|Q3|Q4|-){0,2}(([ ]?[-/.,'][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2})($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(0?[1-9]|1[012])(([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)[0-9]{2})($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2})((([-/.,][ ]*)|([ ]+)))?((January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)((([-/.,][ ]*)|([ ]+)))?(0?[1-9]|[12][0-9]|3[01]))($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2})(([ ]?[-/.,'][ ]*)|([ ]+))(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|Q1|Q2|Q3|Q4){1,3}($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(((10|11|12|13|14|15|16|17|18|19|20)|`)[0-9]{2})(([-/.,][ ]*)|([ ]+))((0?[1-9]|1[012])(([-/.,][ ]*)|([ ]+))(0?[1-9]|[12][0-9]|3[01]))($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2})(([-/.]))((0?[1-9]|1[012])(([-/.,][ ]*)|([ ]+))(0?[1-9]|[12][0-9]|3[01]))($|(?=([^\w]?(\b|\s|$|[)]))))(?!\.\d)""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))((0?[1-9]|1[012])(([-/.][ ]*))(0?[1-9]|[12][0-9]|3[01]))(([-/.][ ]*))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2})($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"""(^|(?<=[(\s.,<:;'"]))([23]{0,1}1st|2?2nd|2?3rd|[12]{0,1}[4-9]th|1[123]th|[123]0th) of (January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)((([-/.,][ ]*)|([ ]+))(((10|11|12|13|14|15|16|17|18|19|20)|`)?[0-9]{2}))?($|(?=([^\w]?(\b|\s|$|[)]))))""")
        self.lstRegex.append(ur"(in|in\sthe\sbeginning\sof|at\sthe\send\sof|since|since\sthe|until|until\sthe\syear|year|after|before|in\syear|in\sthe\syear|in\sthe)\s((19|20)[0-9]{2})s?\b")
        
    def GetPatterns(self):
        patterns = []
    
        for reg in self.lstRegex:
            patterns.append(re.compile(reg,flags=re.UNICODE|re.M|re.I|re.S))
                
        return patterns
    
    def GetMatchedList(self, text):
        matchedlst = []
        
        for y in self.GetPatterns():
            for m in re.finditer(y, text):
                matchedlst.append(WordEntry(m.group(0),m.start(),m.end()))
                
        return matchedlst