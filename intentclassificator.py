import csv
from pathlib import Path
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#Classifies the messages "msg" into 3 different intents with fuzzy wuzzy
def classifyIntent(msg):

    checkMessage(msg)
    choices = ["go to","look around","current room"]
    answer = process.extractOne(msg, choices, scorer=fuzz.partial_ratio)

    return [4, keyToNumber(answer[0])][answer[1] >= 75]

#Returns a number for a specific key
def keyToNumber(argument):
    #all the intents
    checkMessage(argument)
    switcher = {
        "go to":1,
        "look around":2,
        "current room":3,
        "items":4
    }
    # Get the function from switcher dictionary
    return switcher.get(argument,0)

#Returns True if user msg is put to trainingdata.csv otherwise it returns False
def writeMessagetoTrainingData(msg):

    checkMessage(msg)
    filteredmessage = "".join([ c.lower() for c in msg if c.isalnum() or c == ' ' ])
    print(filteredmessage)

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'trainingdata.csv'
    file = file_location.open()

    with open(file_location, 'r', newline = '') as file:
        reader = csv.reader(file, delimiter = '$')
        stringlist = [ " ".join(word) for word in [row for row in reader]]

    with open(file_location, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = '$')

        for string in stringlist:
            if 80 <= fuzz.ratio(filteredmessage, string): return False

        writer.writerow([filteredmessage])
        return True

# Checks if Msg is a String
def checkMessage(msg):
    if not isinstance(msg, str):
        raise ValueError("Message must be of type string")
