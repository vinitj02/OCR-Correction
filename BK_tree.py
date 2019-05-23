import edit_distance

# Max word size
LEN = 30
# Tolerance(In edit distance units)
TOL = 2

class BKTree:
    def __init__(self, word):
        global LEN
        self.word = word
        self.frequency = 0
        self.childrenList = []
        for i in range(0, LEN+1):
            self.childrenList.append(None)
        
    def add(self, curr):
        rootLen = len(self.word)
        currLen = len(curr.word)
        editDistDPMatrix = edit_distance.editDistDP(self.word, curr.word, rootLen, currLen)
        editDist = editDistDPMatrix[rootLen][currLen]
        if(editDist>LEN):
            return
        if self.childrenList[editDist] is None:
            self.childrenList[editDist] = curr                       
        else:
            self.childrenList[editDist].add(curr)   

    def getSimilarWords(self, inputStr, flag):
        global TOL
        global LEN
        similarWordsList = []
        startChild = 1
        endChild = 1
        rootLen = len(self.word)
        inputStrLen = len(inputStr)
        editDistDPMatrix = edit_distance.editDistDP(self.word, inputStr, rootLen, inputStrLen)
        editDist = editDistDPMatrix[rootLen][inputStrLen]
        if(editDist<=TOL):
            if(flag == True):
                similarWordsList.append(self)
            else:    
                similarWordsList.append(self.word)
            endChild = editDist + TOL            
        else:
            startChild = editDist - TOL
            endChild = editDist + TOL
        for i in range(startChild, endChild+1):
            if(i>LEN):
                continue
            if self.childrenList[i] is None:
                continue
            tmpSimilarWordsList = self.childrenList[i].getSimilarWords(inputStr, flag)
            similarWordsList += tmpSimilarWordsList
        return similarWordsList
    
# Driver program 

#==============================================================================
# dictionary = ["hell","help","shel","smell","fell","felt","oops","pop","oouch","halt", "helmet"]     
# 
# root = BKTree("hell")
# 
# for i in dictionary:
#     if(i == "hell"):
#         continue
#     else:
#         curr = BKTree(i)
#         root.add(curr)
#                 
# w1 = "ops"
# w2 = "oops"          
# 
# print(root.getSimilarWords(w1, False))
# print(root.getSimilarWords(w2, False))
#==============================================================================



#==============================================================================
# # Driver program 2
# inputFile = open('Dictionary/updated_eng_words.txt', "r", encoding="utf-8")
# rootWord = inputFile.readline()[:-1]
# root = BKTree(rootWord)
# 
# while True:
#     currWord = inputFile.readline()[:-1]
#     if(len(currWord) == 0):
#         break
#     curr = BKTree(currWord)
#     root.add(curr)
#     
# inputFile.close()
# 
# print(root.getSimilarWords("veij", False))
#==============================================================================
