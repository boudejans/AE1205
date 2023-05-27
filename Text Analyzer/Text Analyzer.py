import os
from matplotlib import pyplot as plt

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

    fileNames = os.listdir(folder)
    if '.DS_Store' in fileNames:
        fileNames.remove('.DS_Store')

    for fileName in fileNames:
        langNames.append(fileName)

        with open(folder + "/" + fileName, 'r', encoding='latin1') as f:
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

# Test character frequency of test file
fileName = input("Enter the name of the text file I should predict the language of: ")
with open(fileName, encoding='utf-8', errors='ignore') as file:
    fileText = file.read().split()
fileFrequency = GetFrequency(fileText)

# Test character frequeny of baseline text files
langNames, langFreqs = GetLanguage("./data")

# Calculate the difference between the test file and each of the 4 languages
differences = []
for i in range(len(langNames)):
    differences.append(GetDifference(fileFrequency, langFreqs[i]))

# Compare character frequency of test file with language baselines
closestLanguageIndex = differences.index(min(differences))
closestLanguage = langNames[closestLanguageIndex]
print("This language is probably: " + closestLanguage.split('.')[0])

# Plot the 4 language frequencies as well as the test frequencies
j = 0
xbar = range(26)
for i in range(321,325):
    plt.subplot(i)
    plt.ylim(0, 0.2)
    plt.title(langNames[j])
    plt.bar(xbar, langFreqs[j][97:123], 0.6, color='r')
    j += 1
plt.subplot(325)
plt.title('Test frequency')
plt.bar(xbar, fileFrequency[97:123], 0.6, color='c')
plt.ylim(0, 0.2)
plt.tight_layout()
plt.show()