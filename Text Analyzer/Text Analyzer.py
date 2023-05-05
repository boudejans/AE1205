import string
import os
import pandas as pd

# Get the character frequency of a list of words
def GetFrequency(txt):
    chrCount = [0] * 8500
    chrFrequency = [0] * 8500
    # Count all the characters in the text
    for wrd in txt:
        for chr in wrd:
            chrCount[ord(chr)] += 1

    # Loop through every possible character and calculate the frequency of that character
    for i in range(len(chrCount)):
        chrFrequency[i] = chrCount[i] / sum(chrCount)

    return chrFrequency

# Get the sample language files and their frequencies from given folder
def GetLanguage(folder):
    langNames = []
    langFreqs = []

    fnames = os.listdir(folder)

    for folderName in fnames:
        langNames.append((folderName))

        with open(folder + "/" + folderName, 'r', encoding='latin1') as f:
            content = f.read().split()
            langFreqs.append(GetFrequency(content))

    return langNames, langFreqs

# Get the frequency difference between two character frequency lists
def GetDifference(freq1, freq2):
    # Loop through every possible character and compare the difference in frequency
    diff = [0] * 8500
    for i in range(len(freq1)):
        diff[i] = (freq1[i] - freq2[i]) ** 2

    return sum(diff)

# Get the index of the minimal difference value
def MinValueIndex(list):
    j = 1
    for i in range(len(list)):
        if j > list[i]:
            j = list[i]
            index = i

    return index

# Test character frequency of test file
fileName = input("Enter the name of the text file I should predict the language of: ")
with open(fileName, 'r', encoding='latin1') as f:
    fileText = f.read().split()
fileFrequency = GetFrequency(fileText)

# Test character frequeny of baseline text files
langNames, langFreqs = GetLanguage("./data")
differences = []
for i in range(len(langNames)):
    differences.append(GetDifference(fileFrequency, langFreqs[i]))

# Compare character frequency of test file with language baselines
closestLanguage = langNames[MinValueIndex(differences)]
print("This language is probably: " + closestLanguage.split(".")[0])
