import edit_distance

def characterLevelAlignment(ocrWord, gtWord, editDistDP, rows, cols):
    if(rows==1 and cols==1):
        return [("","")]
    elif(rows==1 and cols==0):
        return [("","")]
    elif(rows==0 and cols==1):
        return [("","")]
    
    if((rows>=2 and cols>=2) and (ocrWord[rows-2]==gtWord[cols-2])):
        alignedPairsList = characterLevelAlignment(ocrWord, gtWord, editDistDP, rows-1, cols-1)
        for i,pair in enumerate(alignedPairsList):
            (ocr, gt) = pair
            ocr += ocrWord[rows-2]
            gt += gtWord[cols-2]
            pair = (ocr, gt)
            alignedPairsList[i] = pair
        
    else:
        alignedPairsList = []
        if(rows>=2 and cols>=2):
            min_edits = min(editDistDP[rows-2][cols-2], editDistDP[rows-2][cols-1], editDistDP[rows-1][cols-2])
        elif(rows>=2 and cols>=1):
            min_edits = min(editDistDP[rows-2][cols-2], editDistDP[rows-2][cols-1])
        elif(rows>=1 and cols>=2):
            min_edits = min(editDistDP[rows-2][cols-2], editDistDP[rows-1][cols-2])
            
        # Substitution
        if((rows>=2 and cols>=2) and (editDistDP[rows-2][cols-2] == min_edits)):
            tempAlignedPairsList = characterLevelAlignment(ocrWord, gtWord, editDistDP, rows-1, cols-1)
            for i,pair in enumerate(tempAlignedPairsList):
                (ocr, gt) = pair
                ocr += ocrWord[rows-2]
                gt += gtWord[cols-2]
                pair = (ocr, gt)
                tempAlignedPairsList[i] = pair
            alignedPairsList += tempAlignedPairsList
            
        # Deletion    
        if((rows>=2 and cols>=1) and (editDistDP[rows-2][cols-1] == min_edits)):
            tempAlignedPairsList = characterLevelAlignment(ocrWord, gtWord, editDistDP, rows-1, cols)
            for i,pair in enumerate(tempAlignedPairsList):
                (ocr, gt) = pair
                ocr += ocrWord[rows-2]
                gt += "@"
                pair = (ocr, gt)
                tempAlignedPairsList[i] = pair
            alignedPairsList += tempAlignedPairsList
            
        # Insertion  
        if((rows>=1 and cols>=2) and (editDistDP[rows-1][cols-2] == min_edits)):
            tempAlignedPairsList = characterLevelAlignment(ocrWord, gtWord, editDistDP, rows, cols-1)
            for i,pair in enumerate(tempAlignedPairsList):
                (ocr, gt) = pair
                ocr += "@"
                gt += gtWord[cols-2]
                pair = (ocr, gt)
                tempAlignedPairsList[i] = pair
            alignedPairsList += tempAlignedPairsList
    return alignedPairsList

#==============================================================================
# # Driver program 
# ocrWord = "" 
# gtWord = " "
# ocrLen = len(ocrWord)
# gtLen = len(gtWord)
# rows =  ocrLen + 1
# cols =  gtLen + 1          
# editDistDP = edit_distance.editDistDP(ocrWord, gtWord, ocrLen, gtLen)
# print(characterLevelAlignment(ocrWord, gtWord, editDistDP, rows, cols))
#==============================================================================
