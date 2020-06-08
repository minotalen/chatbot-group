import json
import csv
import pandas as pd
import database_SQLite as database
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData
from phone import handleAnswer
import logging_time as l

with open('rooms.json', encoding="utf8") as allLevels:
    data = json.load(allLevels)
    rooms = data['rooms']


def answerHandler(inputjson):
    l.log_start()#logging
    obj = json.loads(inputjson)
    
    if str(obj['mode']) == 'game':
        answer = findAnswer(str(obj['message'].lower()), getRoomId(str(obj['room'])))
    elif str(obj['mode']) == 'phone' and classifyIntent(str(obj['message'].lower()), ['exit phone']) == 1:
        answer = ('You stop looking at the bad quality of your phone', getRoomName(getRoomId(str(obj['room']))), 'game')
    elif str(obj['mode']) == 'phone': 
        answer = [handleAnswer(str(obj['message'].lower())), 'Your Phone', 'phone']
        
    
    if writeMessagetoTrainingData(str(obj['message'])):
        print("added message to training data")
    else:
        print("added nothing to training data")

    # json wird wieder zusammen gepackt
    l.log_time('end')#logging
    l.log_end()#logging
    return json.dumps(
        {"level": 1, "sender": "bot", "room": answer[1], "items": [], "mode": answer[2], "message": answer[0]})


# finds an answer to your message :)
def findAnswer(msg, roomId=-1):
    
    if roomId == -1: raise ValueError("Invalid room id!")
    print(getAllStates(roomId))
 
    choices = ["go to","look at","current room", "items", "about chatbot:", "start phone"]
    intentId = classifyIntent(msg, choices)

    for elem in rooms[roomId]['triggers']:
        if elem is not None:
            if elem['trigName'] in msg:
                return (elem['accept'], getRoomName(roomId), 'game')

    if intentId == 1:
        for elem in rooms[roomId]['objects']:
            if elem['objName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')
        for elem in rooms[roomId]['connections']:
            if elem['conName'] in msg:
                roomId = int(elem['conRoomId'])
                return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

    elif intentId == 2:
        for elem in rooms[roomId]['items']:
            if elem['itemName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')
        for elem in rooms[roomId]['objects']:
            if elem['objName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')

        return (getRoomDescription(roomId), getRoomName(roomId), 'game')

    elif intentId == 3:
        return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

    # elif classifyIntent(msg) == 4:
    #   return (get_inventory(), getRoomName(roomid))

    elif intentId == 5:
        return (aboutHandler(msg), getRoomName(roomId), 'game')

    elif intentId == 6:
        return ('You are now chatting with the professor', getRoomName(roomId), 'phone')

    return ("I have no idea what you want", getRoomName(roomId), 'game')


# CheckIfNone hilfmethode?

"""
Returns the csv file entry specified by the input coordinates
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
"""


def findEntry(id: int, column: int) -> str:
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'roomsGW2.csv'
    file = file_location.open()

    with open(file_location, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='$')
        rooms = [row for row in reader]

    if not len(rooms) > id >= 0 or not len(rooms[id]) > column >= 0:
        return "csv table coordinates are out of range"
    else:
        return rooms[id][column]


# Get the room id by room name
def getRoomId(roomName: str) -> int:
    for count in range(0, len(rooms)):

        if rooms[count]['roomName'] in roomName: return int(rooms[count]['id'])
    else:
        return -1


# Get the current room
def getRoomName(id: int) -> str:
    return rooms[id]['roomName']


# Get introduction of the room with id
def getRoomIntroduction(id: int) -> str:
    return rooms[id]['intro']


# Get description of the room with id
def getRoomDescription(id: int) -> str:
    return rooms[id]['descri']


# Get all needed and new states
def getAllStates(id: int):
    return list(set(getObjectStates(id, 'connections') + 
                    getObjectStates(id, 'items') + 
                    getObjectStates(id,'objects') + 
                    getObjectStates(id, 'triggers')))


# Get states of json object
def getObjectStates(id: int, name: str):
    allStates = []
    if rooms[id][name] is not None:
        for states in rooms[id][name]:
            if states is not None:
                for needState, needStateValue in zip(states['needStates'], states['needStatesValue']):
                    if None not in (needState, needStateValue): allStates.append((needState, needStateValue))
    return allStates


# Check all needed states

# Update states

# Handles about questions
def aboutHandler(msg: str) -> str:
    if "who has" in msg:
        return "I am programmed by student members of the Chatbots:Talk-To-Me Team"
    elif "who" in msg:
        return "I am a Chatbotgame with a browser interface"
    elif "why" in msg:
        return "I was born because the virtualmarsexplporation Project has not enought places for all the students"
    elif "when" in msg:
        return "I was born during the summer semester of 2020"
    elif "what" in msg:
        return "I want to deliver fun and interesting facts about Bremen"
    elif "where" in msg:
        return "I was programmed in Bremen"
    elif "do you like" in msg:
        "of course not"
    else:
        return "I didnt understand your about chatbot: question."


"""
just for Test: Insert user into database by username with dummy password
"""
def add_user_into_db_withoutPassword(username):
    password = "123456"
    if isinstance(username, str):
        database.insert_one_user(username, password)
    else:
        raise ValueError("username must to be in string")


"""
just for Test: Update state with dummy password into database
"""
def update_state_into_DB_withoutPassword(username, state_name, state_value):
    password = "123456"
    if isinstance(username, str) and isinstance(state_name, str) and isinstance(state_value, str):
        database.update_state_users(username, password, state_name, state_value)
    else:
        raise ValueError("input must to be in string")


def add_user_into_db(username, password):
    if isinstance(username, str):
        database.insert_one_user(username, password)
    else:
        raise ValueError("username must to be in string")


def update_state_into_DB(username, password, state_name, state_value):
    if isinstance(username, str) and isinstance(state_name, str) and isinstance(state_value, str):
        database.update_state_users(username, password, state_name, state_value)
    else:
        raise ValueError("input must to be in string")
