import re
class Fact:
    def __init__(self, line, reason):
        self.line = line
        self.reason = reason
    def state(self):
        print(self.line + " because " + self.reason)
have = ["have", "has", "had"]
go = ["go", "goes", "went"]
do = ["do", "does", "did"]
make = ["make", "makes", "made"]
PP = ["seen", "gone", "done", "said"]
modals = ["can", "will", "could", "may", "might", "should",]
tobe = ["am", "is", "are","was", "were"]
f = open("lexical verbs.txt", "r")
text = f.read()
lines = text.split("\n")
vocab = [tobe,modals, have, do, go, make]
for line in lines:
    word = line.split("\t")
    vars()[word[0]] = word
    vocab.append(vars()[word[0]])

def processContractions(txt):
    txt = re.sub("I'm", "I am", txt)
    txt = re.sub("(H|h)e's", "he is", txt)
    txt = re.sub("(S|s)he's", "she is", txt)
    txt = re.sub("(I|i)t's", "it is", txt)
    txt = re.sub("can't", "can not", txt)
    txt = re.sub("cannot", "can not", txt)
    txt = re.sub("'re", " are", txt)
    txt = re.sub("n't", " not", txt)
    txt = re.sub("'t", " not", txt)


    return txt
def makedeclarative(sentence):
    sentence = processContractions(sentence)
#    print(sentence)
    words = sentence.split(" ")
    S = ""
    V = ""
    ARG = ""
    perfect = 0
    for i in range(len(words)):
        #define verbs
        for word in vocab:
            #finds a word that is in its vocab
            #define subject
            if words[i] in word:
                #if it is a to be word
                if words[i] in tobe and V == "":
                    V = words[i]
                    for x in range(0, i):
                        S = S + words[x] + " "
                    S = S.rstrip(" ")
                    S = S.lower()
                    for x in range(i+1, len(words)):
                        ARG = ARG + words[x] + " "
                    ARG = ARG.rstrip(" ")
                if words[i] in do and V == "":
              #      print("do statment!")
                    V = words[i]
                    for x in range(0, i):
                        S = S + words[x] + " "
                    S = S.strip(" ")
                    S = S.lower()
                    for x in range(i+1, len(words)):
                        ARG = ARG + words[x] + " "
                    ARG = ARG.rstrip(" ")
               #     print(ARG)
                
                if words[i] in modals and V == "":
                    
                    #once it has found out if the verb is modal
                    #look for the infinite verb
                    V = words[i]
                    for x in range(0, i):
                        S = S + words[x] + " "
                    S = S.rstrip(" ")
                    S = S.lower()
                    for x in range(i+1, len(words)):
                        ARG = ARG + words[x] + " "
                if words[i] in have and V == "":
                    ## needs to be able to determine
                    ## whether the following clause is a VP
                    ## perhaps by means of a list of past participles?
                    for x in range(i+1, len(words)):
                        ARG = ARG + words[x] + " "
                        if bool(set(ARG.split(" ")) & set(PP)):
                            perfect = 1
                            V = words[i]
                        else:
                            ARG = ""
                            S = ""
                    #ensures that the code doesn't duplicate the subject
                    if perfect == 1:
                        for x in range(0, i):
                            
                            S = S + words[x] + " "
                        S = S.rstrip(" ")
                        S = S.lower()    
                #and V == "" means this lexical verb will only be assigned
                # if a 'to be' verb or modal verb has not yet been found        
                ##write some code that can treat 'to have' in too different ways
                if words[i] not in modals and words[i] not in tobe and V == "" and perfect != 1:
                    V = "do"
                    V2 = words[i]

                    for x in range(0, i):
                        S = S + words[x] + " "
                    S = S.rstrip(" ")
                    S = S.lower()
                    #checks if it is third person singular present
                    if V2 == word[1]:
                        V2 = word[0]
                        V = V + "es"
                    ## write a function that checks if V2 is that last entry
                    ## in its respective word file
                    for word in vocab:
                        if V2 in word:
                            # line below not triggering the code below it
                            #
                            if word.index(V2) == len(word)-1:
                                V = "did"
            #        if V2 in past:
            #            V = "did"
                        #turn a past tense verb into a non-finite one
                    for word in vocab:
                        if V2 in word:
                            V2 = word[0]
                    for x in range(i, len(words)):
                        ARG = ARG + words[x] + " "
                        #makes the verb in the argument finite
                        ARG = ARG.replace(words[i], V2)
                    ARG = ARG.rstrip(" ")
                                
        #check if third personsingular present            
#    print("The subject is: " + S)
#    print("The verb is: " + V)
#    print("The agrument is: " + ARG)
#    return("Why" + " "+ V + " " + S + " " + ARG + "?")
#    print(S + " " + V + " " + ARG)
    #returns a list consisting of these values
    return [S, V, ARG]
def askWhy(SVO):
    question = "Why" + " "+ SVO[1] + " " + SVO[0] + " " + SVO[2] + "?"

    return(question)

    
def changePerson(SVO):
    #checks if the user has said something in the first person
    SVO[0] = SVO[0] + " "
    firsttosecond = re.search("(i|I) ", SVO[0]) or re.search("you", SVO[2])

    if (firsttosecond):
        SVO[0] = re.sub("(i|I) ", "you", SVO[0])
        SVO[1] = re.sub("am", "are", SVO[1])
        SVO[2] = re.sub("you", "me", SVO[2])
        SVO[2] = re.sub("my", "your", SVO[2])
        
    secondtofirst = re.search("(y|Y)ou", SVO[0]) or re.search(" me", SVO[2])
    if (secondtofirst) and not firsttosecond:
        SVO[0] = re.sub("(y|Y)ou$", "I", SVO[0])
        SVO[1] = re.sub("are", "am", SVO[1])
        SVO[2] = re.sub(" me", " you", SVO[2])
        
        
        
    S = SVO[0].rstrip(" ")
    V = SVO[1]
    ARG = SVO[2]
    return[S,V,ARG]
def declarativeToNormal(SVO):
    normal = ""
    if SVO[1] == "did":
        for word in vocab:
            SVO[2] = SVO[2].replace(word[0], word[2])
            SVO[1] = ""
    if SVO[1] == "do":
        for word in vocab:
            SVO[2] = SVO[2].replace(word[0], word[0])
            SVO[1] = ""
    if SVO[1] == "does":
        for word in vocab:
            SVO[2] = SVO[2].replace(word[0], word[1])
            SVO[1] = ""
#    for word in dcl:
#        normal = normal + word + " "
    return SVO
def storeDeclarative(string):
    dcl = changePerson(declarativeToNormal(makedeclarative(string)))
#    print(dcl)
    string = ""
    for word in dcl:
        string = string + word + " "
    return string
def theFunction(string):
    string2 = askWhy(changePerson(makedeclarative(string)))
    return string2
while True:
    txt = input("write something:")
    print(theFunction(txt))
    
