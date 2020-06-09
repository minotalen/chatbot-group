import re
from transformers import pipeline
from intentclassificator import classifyIntent, writeMessagetoTrainingData


text_generator = pipeline("text-generation")

"""
@author:: Max Petendra
@state: 08.06.20
handles the answer of the professor in the game

Parameters
----------
msg: the message of the user

Returns: a string as an answer
"""
def handleAnswer(msg: str) -> str:
    intent = askProf(msg)
    if intent == 1: return "Your task is to play the game"
    return get_generated_answer(msg)

"""
@author:: Max Petendra
@state: 08.06.20
search for intents in the message and ask the prof some defined questions

Parameters
----------
msg: the message of the user

Returns: a number which represent a intent of the user // -1 if no intent is found
"""
def askProf(msg:str) -> str:
    choices = ["tell task"]
    return classifyIntent(msg, choices)

"""
@author:: Max Petendra
@state: 08.06.20
get a  formatted text answer by the traines gpt2 of transformers

Parameters
----------
msg: the message of the user

Returns: a string as an answer
"""
def get_generated_answer(msg: str) -> str:
    text = text_generator(msg, max_length=int(20))[0].get('generated_text')
    for char in "?\n": text = text.replace(char,'')
    proftext = re.sub(msg, '', text)
    splittext = re.split('(?<=[,.!?]) +', proftext)
    if len(splittext) > 1: return re.sub(splittext[-1], '', proftext)
    return proftext

