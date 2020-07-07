import csv
import spacy
from nltk.corpus import wordnet as wn
from pathlib import Path
from fuzzywuzzy import fuzz, process
#from monkeylearn import MonkeyLearn
import logging_time as l

#m1 = MonkeyLearn('9172f7ffa71ad34b35a6c60958566386059cae19')
nlp = spacy.load("en_core_web_sm")

"""
@author:: Max Petendra, Kristin Wünderlich, Tobis -> (logging)
@state: 08.06.20
Classifies the messages "msg" with fuzzywuzzy / monkey learn disabled see comment
Parameters
----------
msg: the user msg to deal with and to search in for meant intents
choices: the list with all the intents to choose must be strings

Returns: Returns the index+1 in choices of the classified intent // -1 if no possible meant intent is found
"""
def classifyIntent(msg: str, choices: list) -> int:
    if not all(isinstance(choice, str) for choice in choices): raise TypeError("intent choices must be a list of strings")
    
    answer = process.extractOne(msg, choices, scorer=fuzz.partial_ratio)
    l.log_time('classify-Intent')#logging
    """
    try: response = m1.classifiers.classify(model_id='cl_bEWrgUGS', data=[msg]).body[0].get("classifications")[0]
    except PlanQueryLimitError as e: print(e.error_code, e.detail)
    except MonkeyLearnException: raise Exception("Something went wrong with Monkey Learn")
          
    answer = [response.get("tag_name"), response.get("confidence")] 
    if not isinstance(answer[0], str) or not isinstance(answer, list) or not isinstance(answer[1], float):
        raise TypeError("MonkeyLearn error created wrong types in the answer")
    """
    return keyToNumber(answer[0], choices) if answer[1] >= 75 else keyToNumber(checkSynonyms(msg, choices), choices)

"""
@author:: Max Petendra
@state: 08.06.20
Get the value a of intent to work with from the list of intents
Parameters
----------
argument: a string which should be a member of choices
choices: the list with all the intents to choose

Returns: Returns a number for a specific intent
"""
def keyToNumber(argument: str, choices: list) -> int:
    if argument in choices: return choices.index(argument) + 1
    else: return -1

"""
@author:: Max Petendra
@state: 08.06.20
filters a string and only alphabethical char and spaces remain
Parameters:
msg : a string to filter
Returns: the filtered string
"""
def filterMessage(msg: str) -> str: return "".join([ c.lower() for c in msg if c.isalpha() or c == ' ' ])

"""
@author:: Max Petendra, Tobias -> (logging time)
@state: 08.06.20
checks which of the given intents are possibly meant
Parameters
----------
msg : the input message of the player to test
choices: the list of intents to choose from

Returns: the intent that has the most consensus with the msg as a string
"""
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

"""
@author:: Max Petendra
@state: 08.06.20
writes the user msg to trainingdata.csv if it is not already in it or a similar msg
Parameters
----------
msg : the input message of the player

Returns: Returns True if user msg is put to trainingdata.csv otherwise it returns False
"""
def writeMessagetoTrainingData(msg: str) -> bool:

    try: msg.decode('utf-8')
    except: return False

    filteredmessage = filterMessage(msg)
    print(filteredmessage)

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'trainingdata.csv'
    file = file_location.open()

    with open(file_location, 'r', newline = '') as file:
        reader = csv.reader(file, delimiter = '$')
        print(reader)
        stringlist = [ " ".join(word) for word in [row for row in reader]]

    with open(file_location, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = '$')

        for string in stringlist:
            if 80 <= fuzz.ratio(filteredmessage, string): return False

        writer.writerow([filteredmessage])
        return True

"""
@author:: Max Petendra
@state: 08.06.20
get set of specific words of a spacy wortype
Parameters
----------
msg : the string to search in
wordtype: must be a valid spacy wordtype 

Returns: all words of a given type in a string as a set
"""
def getWordsofType(msg: str, wordtype: str) -> set:
    result = set()
    pos = nlp(msg)
    for token in pos:
        if str(token.pos_) == wordtype: result.add(token)
    return result

"""
@author:: Max Petendra, Tobias -> (logging)
@state: 08.06.20
checks the similarity of two words
Parameters
----------
word1 : the first word
word2: the second word 

Returns: the number of similar synonyms of two words
"""
def checkSimilarity(word1: str, word2: str) -> int:
    l.log_time('pre-checkSimilarity')#logging
    if not word1.isalpha() or not word2.isalpha():
        raise ValueError("words should only have alpha chars")
    synsofword1 = getSynonyms(word1, getWordtype(word1))
    synsofword2 = getSynonyms(word2, getWordtype(word2))
    l.log_time('post-checkSimilarity')#logging
    return len(set(synsofword1).intersection(synsofword2))

"""
@author:: Max Petendra
@state: 08.06.20
get the synonyms of a word
use getWordtype to get the wordtype of a word
Parameters
----------
word: the word to get synonyms from
wordtype: the wordtype of the synonyms must be a valid spacy wordtype 

Returns: the synonyms of a word as a set
"""
def getSynonyms(word: str, wordtype: str) -> set:
    synonyms = set()
    for syn in wn.synsets(str(word)):
        for lm in syn.lemmas():
            if getWordtype(str(lm.name())) == wordtype:
                synonyms.add(lm.name())
    return sorted(synonyms)

"""
@author:: Max Petendra
@state: 23.06.20
get the wordtype of a word in a give context (optional)
Parameters
----------
word: the word to check the wordtype
sentence: optional: in the given context of a sentence // usually the user msg 

Returns: the spacy wordtype of a word // UNKWOWN if no wordtype is found
"""
def getWordtype(word: str, sentence: str = None) -> str:
    if not word.isalpha() and not '_' in word and not '-' in word:
        return "UNKNOWN"
    if sentence == None : pos = nlp(word)
    else: pos = nlp(sentence)
    for token in pos:
        if str(token) == word: return str(token.pos_)
    return "UNKNOWN"


"""
@author:: Max Petendra
@state: 08.06.20 // !!!! currently unused
Makes a dict from a list. Keys are list elements. Values are numbers from 1 to list length
Parameters:
inputlist : the list with the input strings
Returns: A dictionary of strings and numbers
"""
def listtodict(inputlist: list) -> dict:
    resultdict = {i : inputlist[i-1] for i in range(1, len(inputlist)+1)}
    return {value:key for key, value in resultdict.items()}

