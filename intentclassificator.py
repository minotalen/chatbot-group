import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#Classifies the messages "msg" into 3 different intents with fuzzy wuzzy
def classifyIntent(msg):

    choices = ["go to","look around","current room"]

    answer = process.extractOne(msg, choices, scorer=fuzz.partial_ratio)

    if answer[1] >= 75 :
        return keyToNumber(answer[0])
    
    else: return 4

#Returns a number for a specific key
def keyToNumber(argument):
    #all the intents
    switcher = {
        "go to":1,
        "look around":2,
        "current room":3,
        "items":4
    }
    # Get the function from switcher dictionary
    return switcher.get(argument,0)

def writeMessagetoTrainingData(msg):

    filteredchars = [ c.lower() for c in msg if c.isalnum() or c == ' ' ]
    wordlist = "".join().split()
    
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'trainingdata.csv'
    file = file_location.open()

    with open(file_location, 'r', newline = '') as file:
        reader = csv.reader(file, delimiter='$' )
        stringlist = [ " ".join(word) for word in [row for row in reader]]

    with open(file_location, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = '$')
        similar = False
        for string in stringlist:
            if 80 <= fuzz.ratio("".join(filteredchars), string):
                similar = True
                break

        if similar: writer.writerow(wordlist)        


