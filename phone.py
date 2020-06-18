import re
import json
import logging
import torch
import queue
import database_SQLite as database
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from nltk import tokenize
from intentclassificator import classifyIntent, writeMessagetoTrainingData

# from transformers import pipeline
# text_generator = pipeline("text-generation")

# open json for messages from prof
with open('recmessages.json', encoding="utf8") as messages:
    rec_json = json.load(messages)
    messages = rec_json['messages']

# Initialize tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# Load gpt2 model
model = GPT2LMHeadModel.from_pretrained('gpt2')

rustyprof = "I am completely absent-minded. The proof of my theory is not yet..."

messagequeue = queue.Queue()
#messagequeue = []

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


def handleAnswer(msg: str, username: str, level: int, roomId: int = -1) -> str:
    if roomId == -1:
        raise ValueError("Invalid room id!")
    intent = askProf(msg)
    if intent == 1:
        return "Your task is to play the game"  # replace return with some method
    if intent == 2:
        return printRecentMessage(username)
    # returns the answer of the prof if it is not empty
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


def askProf(msg: str) -> int:
    choices = ["tell task", "print recent message"]
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

    # add . if sentence doesnt end with a punctuation
    input_len = len(input_context)
    if tokenize.sent_tokenize(input_context)[-1][-1] not in "?.,!":
        input_context = input_context + '.'
    input_context = input_context.replace("\n", '')

    # text = text_generator(input_context, max_length=int(20))[0].get('generated_text')
    # for char in "?\n": text = text.replace(char,'')
    # proftext = re.sub(input_context, '', text)
    # splittext = re.split('(?<=[,.!?]) +', proftext)
    # if len(splittext) > 1: print(re.sub(splittext[-1], '', proftext))
    # print(proftext)

    # Encode input with gpt2 tokenizer
    input_ids = tokenizer.encode(input_context, return_tensors='pt')
    outputs = model.generate(
        input_ids=input_ids, max_length=input_len+25, do_sample=True)

    # Postprocessing string
    decoded_text = tokenizer.decode(outputs[0]).format()
    decoded_text = decoded_text.replace('\n', ' ').replace('  ', ' ')
    # better filter for special chars?
    decoded_text = re.sub('\"\'', '', decoded_text)
    answer = decoded_text[input_len:]

    # split into sentences and slice unfinished // returns rustyprof if exception is throwed
    try:
        def formatstart(msg): return msg[2:] if msg[0:2] == '. ' else (
            msg.strip() if msg[0] == ' ' else msg)
        sentences = tokenize.sent_tokenize(answer)
        if len(sentences) > 1:
            return [answer, formatstart(re.sub(sentences[-1], '', answer)).rstrip()][len(answer) > 2]
        return [answer, formatstart(answer).rstrip()][len(answer) > 2]
    except:
        return rustyprof


"""
@author:: Max Petendra, Jakob Hackstein
@state: 17.06.20
adds message to message queue if message is triggerd

Parameters
----------
username: the username of the current player as a string

Returns: the last sent message of the prof (from the messagequeue)
"""


def printRecentMessage(username) -> str:
    for msgdict in messages:
        if database.get_user_state_value(
                username, msgdict.get("user_state"), False):
            if not database.does_user_recmessage_exist(username, msgdict.get("id")):
                messagequeue.put(msgdict.get("str_message"))
                database.insert_user_recmessage(username, msgdict.get("id"))
        else:
            print("user state of msg is not in database yet")
     
    return "you have no new messages yet" if messagequeue.empty() else messagequeue.get()
    


def getAllMessages(username):
    allmessages = []
    for msgdict in messages:
        if database.does_user_recmessage_exist(username, msgdict.get("id")):
            allmessages += msgdict.get("str_message")
    return(allmessages)
