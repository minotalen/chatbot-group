import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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



