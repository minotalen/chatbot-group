import csv
#import spacy
#from nltk.corpus import wordnet as wn
from pathlib import Path
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from monkeylearn import MonkeyLearn

#m1 = MonkeyLearn('9172f7ffa71ad34b35a6c60958566386059cae19')
#nlp = spacy.load("en_core_web_sm")

#Classifies the messages "msg" with fuzzywuzzy / monkey learn disabled see comment
def classifyIntent(msg: str) -> int:

    choices = ["go to","look around","current room", "items", "about chatbot:"]
    answer = process.extractOne(msg, choices, scorer=fuzz.partial_ratio)

    """
    try: response = m1.classifiers.classify(model_id='cl_bEWrgUGS', data=[msg]).body[0].get("classifications")[0]
    except PlanQueryLimitError as e: print(e.error_code, e.detail)
    except MonkeyLearnException: raise Exception("Something went wrong with Monkey Learn")
          
    answer = [response.get("tag_name"), response.get("confidence")] 
    if not isinstance(answer[0], str) or not isinstance(answer, list) or not isinstance(answer[1], float):
        raise TypeError("MonkeyLearn error created wrong types in the answer")
    """
    
    return [6, keyToNumber(answer[0])][answer[1] >= 75] #0.175

#Returns a number for a specific key
def keyToNumber(argument: str) -> int:
    #all the intents
    switcher = {
        "go to":1,
        "look around":2,
        "current room":3,
        "items":4,
        "about chatbot:":5
    }
    # Get the function from switcher dictionary
    return switcher.get(argument, 6)

#Returns True if user msg is put to trainingdata.csv otherwise it returns False
def writeMessagetoTrainingData(msg: str) -> bool:

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

#returns the synonyms of a word // use getWordtype to get the wordtype of a word
"""
def getSynonyms(word: str, wordtype: str) -> set:
    synonyms = set()
    for syn in wn.synsets(str(word)):
        for lm in syn.lemmas():
            if getWordtype(str(lm.name())) == wordtype:
                synonyms.add(lm.name())
    return sorted(synonyms)
"""
#returns the wordtype of a word // optional: in the given context of a sentence
"""
def getWordtype(word: str, sentence: str = None) -> str:
    if not word.isalpha() and not '_' in word: raise ValueError("word should only contain alpha chars")
    if sentence == None : pos = nlp(word)
    else: pos = nlp(sentence)
    for token in pos:
        if str(token) == word: return str(token.pos_)
    raise Exception("sentence does not contain the word")
"""