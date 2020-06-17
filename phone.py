import re
import logging
import torch
import queue
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from nltk import tokenize
from intentclassificator import classifyIntent, writeMessagetoTrainingData

# from transformers import pipeline
# text_generator = pipeline("text-generation")


# Initialize tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# Load gpt2 model
model = GPT2LMHeadModel.from_pretrained('gpt2')

rustyprof = "I am completely absent-minded. The proof of my theory is not yet..."

messagequeue = queue.Queue()

"""
@author:: Max Petendra
@state: 10.06.20
handles the answer of the professor in the game
// idea if intent is classifier execute method with room and level
so you get apropiate information from the prof

Parameters
----------
msg: the message of the user
level: the current level of the player as an int

Returns: a string as an answer
"""
def handleAnswer(msg: str, level: int, roomId: int = -1) -> str:
    if roomId == -1: raise ValueError("Invalid room id!")
    intent = askProf(msg)
    if intent == 1: return "Your task is to play the game" #replace return with some method

    #returns the answer of the prof if it is not empty
    answer = get_generated_answer(msg)
    return [answer, rustyprof][not answer]


"""
@author:: Max Petendra
@state: 08.06.20
search for intents in the message and ask the prof some defined questions

Parameters
----------
msg: the message of the user

Returns: a number which represent a intent of the user // -1 if no intent is found
"""
def askProf(msg:str) -> int:
    choices = ["tell task"]
    return classifyIntent(msg, choices)

"""
@author:: Max Petendra, Jakob Hackstein
@state: 15.06.20
get a  formatted text answer by transformers using a pretrained gpt-2

Parameters
----------
msg: the message of the user

Returns: a string as an answer
"""
def get_generated_answer(input_context: str) -> str:

    #add . if sentence doesnt end with a punctuation
    input_len = len(input_context)
    if tokenize.sent_tokenize(input_context)[-1][-1] not in "?.,!": input_context = input_context + '.'
    input_context = input_context.replace("\n",'')
    
    # text = text_generator(input_context, max_length=int(20))[0].get('generated_text')
    # for char in "?\n": text = text.replace(char,'')
    # proftext = re.sub(input_context, '', text)
    # splittext = re.split('(?<=[,.!?]) +', proftext)
    # if len(splittext) > 1: print(re.sub(splittext[-1], '', proftext))
    # print(proftext)

    # Encode input with gpt2 tokenizer
    input_ids = tokenizer.encode(input_context, return_tensors='pt')
    outputs = model.generate(input_ids=input_ids, max_length=input_len+25, do_sample=True)

    # Postprocessing string
    decoded_text = tokenizer.decode(outputs[0]).format()
    decoded_text = decoded_text.replace('\n', ' ').replace('  ', ' ')
    decoded_text = re.sub('\"\'','', decoded_text) # better filter for special chars?
    answer = decoded_text[input_len:]
    
    # split into sentences and slice unfinished // returns rustyprof if exception is throwed
    try:
        formatstart = lambda msg: msg[2:] if msg[0:2] == '. ' else (msg.strip() if msg[0] == ' ' else msg)
        sentences = tokenize.sent_tokenize(answer)
        if len(sentences) > 1: return [answer, formatstart(re.sub(sentences[-1], '', answer)).rstrip()][len(answer)>2]
        return [answer, formatstart(answer).rstrip()][len(answer)>2]
    except: return rustyprof   


