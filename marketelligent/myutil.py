import re



def normalize(f):
    f = [x.lower() for x in f]
    f = [x.replace("\\n"," ") for x in f]        
    f = [x.replace("\\t"," ") for x in f]        
    f = [x.replace("\\xa0"," ") for x in f]
    f = [x.replace("\\xc2"," ") for x in f]

    #f = [x.replace(","," ").replace("."," ").replace(" ", "  ") for x in f]
    #f = [re.subn(" ([a-z]) ","\\1", x)[0] for x in f]  
    #f = [x.replace("  "," ") for x in f]

    f = [x.replace(" u "," you ") for x in f]
    f = [x.replace(" em "," them ") for x in f]
    f = [x.replace(" da "," the ") for x in f]
    f = [x.replace(" yo "," you ") for x in f]
    f = [x.replace(" ur "," you ") for x in f]
    #f = [x.replace(" ur "," your ") for x in f]
    #f = [x.replace(" ur "," you're ") for x in f]
    
    f = [x.replace("won't", "will not") for x in f]
    f = [x.replace("can't", "cannot") for x in f]
    f = [x.replace("i'm", "i am") for x in f]
    f = [x.replace(" im ", " i am ") for x in f]
    f = [x.replace("ain't", "is not") for x in f]
    f = [x.replace("'ll", " will") for x in f]
    f = [x.replace("'t", " not") for x in f]
    f = [x.replace("'ve", " have") for x in f]
    f = [x.replace("'s", " is") for x in f]
    f = [x.replace("'re", " are") for x in f]
    f = [x.replace("'d", " would") for x in f]

    #f = [x.replace("outta", "out of") for x in f]

#     bwMap = loadBW()
#     for key, value in bwMap.items():
#         kpad = " " + key + " "
#         vpad = " " + value + " "
#         f = [x.replace(kpad, vpad) for x in f]
        
    # stemming    
#     f = [re.subn("ies( |$)", "y ", x)[0].strip() for x in f]
#     #f = [re.subn("([abcdefghijklmnopqrstuvwxyz])s( |$)", "\\1 ", x)[0].strip() for x in f]
#     f = [re.subn("s( |$)", " ", x)[0].strip() for x in f]
#     f = [re.subn("ing( |$)", " ", x)[0].strip() for x in f]
#     f = [x.replace("tard ", " ") for x in f]
#         
#     f = [re.subn(" [*$%&#@][*$%&#@]+"," xexp ", x)[0].strip() for x in f]
# #     f = [re.subn(" [0-9]+ "," DD ", x)[0].strip() for x in f]
#     f = [re.subn("<\S*>","", x)[0].strip() for x in f]    
    return f