import string
import os


# Get the character frequency of a list of words
def GetFrequency(txt):
    chrCount = [0] * 26
    chrFrequency = [0] * 26
    for wrd in txt:
        for chr in wrd:
            chrCount[string.ascii_lowercase.index(chr)] += 1

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

        with open(folder + "/" + folderName) as f:
            content = f.read().split()
            langFreqs.append(GetFrequency(content))

    return langNames, langFreqs

# Get the frequency difference between two character frequency lists
def GetDifference(freq1, freq2):
    diff = [0] * 26
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


fileName = input("Enter the name of the text file I should predict the language of: ")
with open(fileName) as f:
    fileText = f.read().split()
fileFrequency = GetFrequency(fileText)

langNames, langFreqs = GetLanguage("./data")
differences = []
for i in range(len(langNames)):
    differences.append(GetDifference(fileFrequency, langFreqs[i]))

closestLanguage = langNames[MinValueIndex(differences)]
print("This language is probably: " + closestLanguage.split(".")[0])
