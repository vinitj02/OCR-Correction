# OCR-Correction

Objective of this project is to solve English token errors in OCR output for Post-OCR Text Correction competition by ICDAR.
•	Input: Erroneous English Token
e.g. – hlmtt

•	Output: Corrected English Token
e.g. – helmet

#############
Model - 1 
#############

•	Character set: (a-z); (A-Z); (@)

•	Data (Train directory - ICDAR_train_without_punc, Test directory - ICDAR_test_without_punc) </br>
All the data is converted into the form of (incorrect token, correct token) pairs
The pairs are extracted from the ICDAR dataset as follows:
1. The incorrect token is taken from the OCR output in the ICDAR dataset and the corresponding correct token is taken from the ground truth in the dataset
2. Both of these are then removed of any punctuations, spaces or special characters except the ones in the defined character set

•	Dictionary - (directory - Dictionary/frequency_dict_without_punc.txt)</br>
Our first model is vocabulary based, so we use a dictionary
We modify the dictionary by updating the frequency of the words by counting their occurences in the dataset. In this process, we also add the new words from the 
dataset into the dictionary

•	Motivation for the first model </br>
Using the training data to learn the error patterns using character confusion probabilities thereby trying to learn which ngrams are being repeatedly misunderstood
in the OCR output

•	To Run </br>
Requirements - Python3
Program to run - ocr_correction.py
Output - Wait around 8-10 minutes for the program to print output since the making and searching BK tree with around 400000 nodes takes time
Only the tokens that were properly corrected are printed in the below form - </br>
#############Corrected Output################</br>
Incorrect English Token:  ano
Corrected English Token:  and
Ground Truth English Token:  and
#############################################</br>

Accuracy - 38% where the test dataset consists of only incorrect tokens removed of punctuations </br>
Accuracy - 52.5% where the test dataset consists of only incorrect tokens which didn't have punctuations in the first place (ICDAR_test_trivial)
