import edit_distance
import BK_tree
import character_level_alignment
import os

# Total number of files
F = 100

#Root for the BK Tree
root = None

# Total Words in Training dataset
totalWordFrequency = 0

# Number of distinct words in vocabulary(dictionary)
vocabularySize = 376661

# Confusion Dictionary
confusionDict = {}
ngram = 2
totalChar = 53 # @, A-Z, a-z


# Considering @, A-Z, a-z
def charToNum(c):
    num = ord(c)
    if(num>=64 and num<=90):
        return(num-64)
    elif(num>=97 and num<=122):
        return(num-97+27)

def createConfusionDictionary(ngram, totalChar):
    for i in range(ngram):
        rows = totalChar**(i+1)
        cols = rows
        tempConfusionMatrix = [[0 for x in range(rows)] for x in range(cols)]
        confusionDict[i+1] = tempConfusionMatrix

# ocrArrLen = gtArrLen = finalArrLen         
def updateConfusionDictionary(ocrWord, gtWord, ngram, totalChar):
    finalWordLen = len(ocrWord)
    for i in range(ngram):
        for j in range(0,finalWordLen-i):
            row = 0
            col = 0
            for k in range(j, j+i+1):
                row += totalChar**(j+i-k) * charToNum(ocrWord[k])
                col += totalChar**(j+i-k) * charToNum(gtWord[k])
            confusionDict[i+1][row][col] +=1    

                      
#==============================================================================
# Create Confusion Dictionary                           
#==============================================================================
createConfusionDictionary(ngram, totalChar)
             
#==============================================================================
# Update Confusion Dictionary              
#==============================================================================
faultInDataset = 0 # Unequal ocrword and gtword
for i in range(F):
    filePath = 'ICDAR_train_final_without_punc/' + str(i) + ".txt"
    exists = os.path.isfile(filePath)
    if exists:
        inputFile1 = open(filePath, "r", encoding="utf-8")
        allLines = inputFile1.readlines()
        inputFile1.close()
        for j in range (0,len(allLines)):
            ocrWord, gtWord = allLines[j][:-1].split(" , ")
            if(len(ocrWord)!=len(gtWord)):
                faultInDataset+=1
                continue
            else:
                totalWordFrequency+=1
            updateConfusionDictionary(ocrWord, gtWord, ngram, totalChar)


def calculateConfusionDictProb(ngram, totalChar):
    totalList = []
    for i in range(ngram):
        tempTotalList = [0 for x in range(len(confusionDict[i+1]))]
        for j in range(len(confusionDict[i+1])):
            tempTotal = 0
            for k in range(len(confusionDict[i+1][0])):
                tempTotal += confusionDict[i+1][j][k]
            tempTotalList[j] = tempTotal
        totalList.append(tempTotalList)
    # Applying Laplace Smoothing (Probability(character) = (frequency of character + 1)/(Total frequency + Total distinct characters))    
    for i in range(ngram):
        for j in range(len(confusionDict[i+1])):
            for k in range(len(confusionDict[i+1][0])):
                confusionDict[i+1][j][k]+=1
                confusionDict[i+1][j][k]/=(totalList[i][j] + totalChar**(i+1))             


#==============================================================================
# Calculate Confusion Dictionary Probability
#==============================================================================
calculateConfusionDictProb(ngram, totalChar)


#==============================================================================
# Create BK Tree 
#==============================================================================
inputFile2 = open('Dictionary/frequency_dict_without_punc.txt', "r", encoding="utf-8")
rootData = inputFile2.readline()[:-1]
rootWord, rootFrequency = rootData.split(" , ")
root = BK_tree.BKTree(rootWord)
root.frequency = int(rootFrequency)

while True:
    currData = inputFile2.readline()[:-1]
    if(len(currData) == 0):
        break
    currWord, currFrequency = currData.split(" , ")
    curr = BK_tree.BKTree(currWord)
    curr.frequency = int(currFrequency)
    root.add(curr)
    
inputFile2.close()

 
# incWordLen = probableWordLen = finalWordLen
def probabilisticFiltering(alignedProbableList, ngram):
    scoreDict = {}
    for pair in alignedProbableList:
        for wordPair in pair[0]:
            incWord = wordPair[0]
            probableWord = wordPair[1]
            finalWordLen = len(incWord)
            ngramWiseProbability = []
            for i in range(ngram):
                prob = 1
                for j in range(0,finalWordLen-i):
                    row = 0
                    col = 0
                    for k in range(j, j+i+1):
                        row += totalChar**(j+i-k) * charToNum(incWord[k])
                        col += totalChar**(j+i-k) * charToNum(probableWord[k])
                    prob*=confusionDict[i+1][row][col]
                prob*=((pair[1]+1)/(totalWordFrequency + vocabularySize))    
                ngramWiseProbability.append(prob)    
            scoreDict[(incWord, probableWord)] = ngramWiseProbability    
    return scoreDict              

#==============================================================================
# Testing     
#==============================================================================        
totalTestExamples = 0
correctedTestExamples = 0
inputFile4 = open('ICDAR_test_without_punc/test_token_pairs.txt', "r", encoding="utf-8")
while(True):
    inputLine = inputFile4.readline()[:-1]
    if(len(inputLine) == 0):
        break    
    token, gtWord = inputLine.split(" , ")
    incWord = ""
    capFlag = False
    for c in token:
        if((c>="\u0041" and c<="\u005A") or (c>="\u0061" and c<="\u007A")):
            incWord+=c
    if(incWord!=""):
        if(incWord[0]>="\u0041" and incWord[0]<="\u005A"):
            capFlag = True
    probableNodeList = root.getSimilarWords(incWord, True)
    alignedProbableList = []
    incLen = len(incWord)
    rows =  incLen + 1
    for probableNode in probableNodeList:
        probableWord = probableNode.word
        probableFrequency = probableNode.frequency
        probableLen = len(probableWord)
        cols =  probableLen + 1  
        duplicate = False
        if(capFlag==True):
            if(probableWord[0]>="\u0061" and probableWord[0]<="\u007A"):
                if(probableLen>1):
                    probableWord = chr(ord(probableWord[0])-(97-65)) + probableWord[1:]
                else:
                    probableWord = chr(ord(probableWord[0])-(97-65))
                probableFrequency = 0
                for tempProbableNode in probableNodeList:
                    if(probableWord == tempProbableNode.word):
                        duplicate = True
                        break
        if(duplicate == False):        
            editDistDP = edit_distance.editDistDP(incWord, probableWord, incLen, probableLen)
            alignedProbableList.append((character_level_alignment.characterLevelAlignment(incWord, probableWord, editDistDP, rows, cols), probableFrequency))
            
    scoreDict = probabilisticFiltering(alignedProbableList, ngram)
    topScoreDict = sorted(scoreDict.items(), key = lambda kv:(kv[1][1], kv[0]), reverse = True)[:6]
    for element in topScoreDict:
        alignedProbableWord = element[0][1]
        correspondingScore = element[1][1]
        if(alignedProbableWord == gtWord):
            print("#############Corrected Output################")
            print("Incorrect English Token: ", incWord)
            print("Corrected English Token: ", alignedProbableWord)
            print("Ground Truth English Token: ", gtWord)
            print("#############################################")
            correctedTestExamples+=1
            break
    totalTestExamples+=1

inputFile4.close()

print("Accuracy: " + str((correctedTestExamples/totalTestExamples)*100) + " %")
