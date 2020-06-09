import json
import csv
import pandas as pd
import database_SQLite as database
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData
from phone import handleAnswer
from riddlemode import handleRiddle
import logging_time as l

with open('rooms.json', encoding="utf8") as allLevels:
    data = json.load(allLevels)
    rooms = data['rooms']


def answerHandler(inputjson):
    l.log_start()#logging
    obj = json.loads(inputjson)
    
    #When the mode is phone and player inputs exit phone
    if str(obj['mode']) == 'phone' and classifyIntent(str(obj['message'].lower()), ['exit phone']) == 1:
        answer = ('You stop looking at the bad quality of your phone', getRoomName(getRoomId(str(obj['room']))), 'game')
        
    #When the mode is phone   
    elif str(obj['mode']) == 'phone': 
        #answer = [handleAnswer(str(obj['message'].lower())), 'Your Phone', 'phone']
        answer = ['you are still talking to th professor', 'Your Phone', 'phone']

    #When the mode is riddle
    elif str(obj['mode']) == 'riddle':
        answer = handleRiddle(obj)
        
    #When mode is game    
    else :
        answer = findAnswer(str(obj['message'].lower()), getRoomId(str(obj['room'])))

        #Case Trigger: Ein trigger wird ausgelöst und eventuell ändern sich zustände, funktionen werden ausgeführt

        """
        #Ist der benötigte Zustand erreicht? Wenn nicht gebe fail text aus
        #Falls einer existiert:
        beZustand = rooms[id][trigger]['benötigterzustand']
        beZustandStatus = rooms[id][trigger]['benötigterzustandstatus']
        
        if(sql[beZustand].status != beZustandStatus)
            answer[0] = "You can't do that"
            
        for every item in items
            checkItemin Inventory(item)
            answer[0] = failtext

        if zustand erfolgreich && zustände erfolgreich:
        
            #Das nächste nur ausführen wenn item und beZustände erfolgreich waren    
            #Ändere zustände die durch trigger geändert werden    
            for every zustand in neuezustände
                neuZustand = rooms[id][trigger]['neuerzustand']
                neuZustandStatus = rooms[id][trigger]['neuerzustandstatus']
                sql[neuZustand].status = neuZustandStatus
            
            #führe funktionen aus des triggers aus
            for every action in Aktionen
                handleTriggerAction(rooms[actions],rooms[actionValue])
        
        """
        
    
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
 
    choices = ["go to","look at","current room", "items", "about chatbot:", "start phone"]
    intentId = classifyIntent(msg, choices)

    #TRIGGER: Raumspezifische Trigger werden zuerst überprüft
    for elem in rooms[roomId]['triggers']:
        if elem is not None:
            if elem['trigName'] in msg:
                return (elem['accept'], getRoomName(roomId), 'game')
            
    #GO TO: Es kann zu anliegenden Räumen oder Objekten gegangen werden
    if intentId == 1:
        for elem in rooms[roomId]['connections']:
            if elem['conName'] in msg:
                roomId = int(elem['conRoomId'])
                return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')
        for elem in rooms[roomId]['objects']:
            if elem['objName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')
        
    #LOOK AT: Items und Objekte im Raum können angeschaut werden. ansonsten wird LOOK AROUND die Raumbeschreibungs ausgegeben
    elif intentId == 2:
        for elem in rooms[roomId]['items']:
            if elem['itemName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')
        for elem in rooms[roomId]['objects']:
            if elem['objName'] in msg:
                return (elem['lookAt'], getRoomName(roomId), 'game')

        return (getRoomDescription(roomId), getRoomName(roomId), 'game')

    #CURRENT ROOM: Gibt den Raumtext nochmal aus
    elif intentId == 3:
        return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

    #ITEMS: NOCH NICHT FERTIG. BAUSTELLE
    # elif classifyIntent(msg) == 4:
    #   return (get_inventory(), getRoomName(roomid))
    
    #ABOUT: Beantwortet Fragen zum Chatbot
    elif intentId == 5:
        return (aboutHandler(msg), getRoomName(roomId), 'game')
    #START PHONE: Der Handymodus wird gestartet
    elif intentId == 6:
        return ('You are now chatting with the professor', getRoomName(roomId), 'phone')
    
    #Wenn nichts erkannt wurde
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


# Check states of room.json in specified category
def checkRoomStates(id: int, name: str):
    
    if rooms[id][name] is not None:
        for states in rooms[id][name]:
            if states is not None:
                for needState, needStateValue in zip(states['needStates'], states['needStatesValue']):
                    if None not in (needState, needStateValue): return True

    return False


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

