import csv
import spacy
from nltk.corpus import wordnet as wn
from pathlib import Path
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from monkeylearn import MonkeyLearn
import logging_time as l

#m1 = MonkeyLearn('9172f7ffa71ad34b35a6c60958566386059cae19')
nlp = spacy.load("en_core_web_sm")

#Classifies the messages "msg" with fuzzywuzzy / monkey learn disabled see comment
def classifyIntent(msg: str) -> int:
    
    choices = ["go to","look at","current room", "items", "about chatbot:", "start phone", "exit phone"]
    answer = process.extractOne(msg, choices, scorer=fuzz.partial_ratio)
    l.log_time('1')#logging
    """
    try: response = m1.classifiers.classify(model_id='cl_bEWrgUGS', data=[msg]).body[0].get("classifications")[0]
    except PlanQueryLimitError as e: print(e.error_code, e.detail)
    except MonkeyLearnException: raise Exception("Something went wrong with Monkey Learn")
          
    answer = [response.get("tag_name"), response.get("confidence")] 
    if not isinstance(answer[0], str) or not isinstance(answer, list) or not isinstance(answer[1], float):
        raise TypeError("MonkeyLearn error created wrong types in the answer")
    """
    return [keyToNumber(checkSynonyms(msg, choices)), keyToNumber(answer[0])][answer[1] >= 75] #0.175

#Returns a number for a specific key
def keyToNumber(argument: str) -> int:
    l.log_time('key')#logging
    #all the intents
    switcher = {
        "go to":1,
        "look at":2,
        "current room":3,
        "items":4,
        "about chatbot:":5,
        "start phone":6,
        "exit phone":7
    }
    # Get the function from switcher dictionary
    l.log_time('toNumber')#logging
    return switcher.get(argument, -1)

def filterMessage(msg: str) -> str: return "".join([ c.lower() for c in msg if c.isalnum() or c == ' ' ])

# check with of the given intents are possibly meant // returns it
def checkSynonyms(msg: str, choices: list) -> str:
    l.log_time('check')#logging
    listofwords = filterMessage(msg).split()
    l.log_time('filter')#logging
    typeofwords =  list(map(lambda x: getWordtype(x, ' '.join(listofwords)), listofwords))
    l.log_time('typeofwords')#logging
    wordsandtype = list(zip(listofwords, typeofwords))
    l.log_time('wordsandtype')#logging    
    listofchoices = list(map(lambda x: filterMessage(x).split(), choices))
    l.log_time('listofchoices')#logging  
    results = []
    l.log_time('pre-loop')#logging
    for intent in listofchoices:
        results.append(0)
        for body in intent:
            wordratings = [0]
            for tup in wordsandtype:
                if tup[1] == getWordtype(body):
                   wordratings.append(checkSimilarity(body, tup[0]))
                   results[len(results)-1] += max(wordratings)
    l.log_time('post-loop')#logging
    return ["i dont know", choices[results.index(max(results))]][max(results) > 0]               

#Returns True if user msg is put to trainingdata.csv otherwise it returns False
def writeMessagetoTrainingData(msg: str) -> bool:

    filteredmessage = filterMessage(msg)
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


#Returns all words of a given type in a string // wordtype must be a valid spacy wordtype
def getWordsofType(msg: str, wordtype: str) -> set:
    result = set()
    pos = nlp(msg)
    for token in pos:
        if str(token.pos_) == wordtype: result.add(token)
    return result

#checks the similarity of two words // returns the number of similar synonyms of two words
def checkSimilarity(word1: str, word2: str) -> int:
    l.log_time('pre-checkSimilarity')#logging
    if not word1.isalpha() or not word2.isalpha():
        raise ValueError("words should only have alpha chars")
    synsofword1 = getSynonyms(word1, getWordtype(word1))
    synsofword2 = getSynonyms(word2, getWordtype(word2))
    l.log_time('post-checkSimilarity')#logging
    return len(set(synsofword1).intersection(synsofword2))

#returns the synonyms of a word // use getWordtype to get the wordtype of a word
def getSynonyms(word: str, wordtype: str) -> set:
    synonyms = set()
    for syn in wn.synsets(str(word)):
        for lm in syn.lemmas():
            if getWordtype(str(lm.name())) == wordtype:
                synonyms.add(lm.name())
    return sorted(synonyms)

#returns the wordtype of a word // optional: in the given context of a sentence
def getWordtype(word: str, sentence: str = None) -> str:
    if not word.isalpha() and not '_' in word and not '-' in word:
        raise ValueError("word should only contain alpha chars")
    if sentence == None : pos = nlp(word)
    else: pos = nlp(sentence)
    for token in pos:
        if str(token) == word: return str(token.pos_)
    return "UNKNOWN"

