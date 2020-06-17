import json
import pandas as pd
import database_SQLite as database
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData
from phone import handleAnswer
from riddlemode import checkAnswer
import logging_time as l

with open('rooms.json', encoding="utf8") as allLevels:
    data = json.load(allLevels)
    rooms = data['rooms']


def answerHandler(inputjson, username):
    l.log_start()  # logging
    obj = json.loads(inputjson)

    # When the mode is phone and player inputs exit phone
    if str(obj['mode']) == 'phone' and classifyIntent(str(obj['message'].lower()), ['exit phone']) == 1:
        answer = ('You stop looking at the bad quality of your phone', getRoomName(getRoomId(str(obj['room']))), 'game')

    # When the mode is phone
    elif str(obj['mode']) == 'phone':
        answer = [handleAnswer(str(obj['message'].lower()), username, int(obj['level']), getRoomId(str(obj['room']))),
                  getRoomName(getRoomId(str(obj['room']))), 'phone']

    # When the mode is riddle
    elif str(obj['mode']) == 'riddle':
        answer = checkAnswer(str(obj['message'].lower()), getRoomId(str(obj['room'])), username)
        answer[1]= getRoomName(answer[1])

    # When mode is game
    else:
        answer = findAnswer(username, str(obj['message'].lower()), getRoomId(str(obj['room'])))

        # Case Trigger: Ein trigger wird ausgelöst und eventuell ändern sich zustände, funktionen werden ausgeführt

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
    l.log_time('end')  # logging
    l.log_end()  # logging
    return json.dumps(
        {"level": 1, "sender": "bot", "room": answer[1], "items": [], "mode": answer[2], "message": answer[0]})


# finds an answer to your message :)
def findAnswer(username, msg, roomId=-1):
    if roomId == -1: raise ValueError("Invalid room id!")

    choices = ["go to", "look at", "pick up", "items", "current room", "about chatbot:", "start phone", "help assistant:"]

    elemCount = -1
    # TRIGGER: Raumspezifische Trigger werden zuerst überprüft // please write docs in english :''(
    for elem in rooms[roomId]['triggers']:
        if elem is not None:
            elemCount += 1
            if elem['trigName'] in msg and checkNeededStates(rooms[roomId]['triggers'][elemCount], username):
                updateStates(rooms[roomId]['triggers'][elemCount], username)
                altMode = 'game'
                altRoom = roomId
                if elem['actions'][0] is not None:
                    for action, actionValue in zip(elem['actions'], elem['actionsValue']):
                        altAction = doAction(action, actionValue, roomId, username)
                        if altAction[0] is not None: altRoom = altAction[0]
                        elif altAction[1] is not None: altMode = altAction[1]
                return (elem['accept'], getRoomName(altRoom), altMode)
            elif elem['trigName'] in msg:
                return (elem['fail'], getRoomName(roomId), 'game')

    intentID = classifyIntent(msg, choices)

    # GO TO: Es kann zu anliegenden Räumen oder Objekten gegangen werden
    if intentID == 1:
        elemCount = -1
        # RÄUME
        for elem in rooms[roomId]['connections']:
            elemCount += 1
            for name in elem['conNames']:
                if name in msg and checkNeededStates(rooms[roomId]['connections'][elemCount], username):
                    roomId = int(elem['conRoomId'])
                    return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')
        elemCount = -1
        # OBJEKTE
        for elem in rooms[roomId]['objects']:
            elemCount += 1
            if elem['objName'] in msg and checkNeededStates(rooms[roomId]['objects'][elemCount], username):
                updateStates(rooms[roomId]['objects'][elemCount], username)
                return (elem['lookAt'], getRoomName(roomId), 'game')

    # LOOK AT: Items und Objekte im Raum können angeschaut werden. ansonsten wird LOOK AROUND die Raumbeschreibungs ausgegeben
    elif intentID == 2:
        elemCount = -1
        # ITEMS
        if rooms[roomId]['items'][0] is not None:
            for elem in rooms[roomId]['items']:
                elemCount += 1
                if elem['itemName'] in msg and checkNeededStates(rooms[roomId]['items'][elemCount], username):
                    return (elem['lookAt'], getRoomName(roomId), 'game')
                
        elemCount = -1
        # OBJEKTE
        if rooms[roomId]['items'][0] is not None:
            for elem in rooms[roomId]['objects']:
                elemCount += 1
                if elem['objName'] in msg and checkNeededStates(rooms[roomId]['objects'][elemCount], username):
                    updateStates(rooms[roomId]['objects'][elemCount], username)
                    return (elem['lookAt'], getRoomName(roomId), 'game')

        return (getRoomDescription(roomId), getRoomName(roomId), 'game')

    # PICK UP: Hebt ein item auf und gibt den Text zurück
    elif intentID == 3:
        elemCount = -1
        for elem in rooms[roomId]['items']:
            elemCount += 1
            if elem['itemName'] in msg and checkNeededStates(rooms[roomId]['items'][elemCount], username):
                updateStates(rooms[roomId]['items'][elemCount], username)
                add_to_inventory(elem['itemName'], roomId, username)
                return (elem['pickUp'], getRoomName(roomId), 'game')
    
    # ITEMS: NOCH NICHT FERTIG. BAUSTELLE
    elif intentID == 4:
        return (get_inventory(roomId, username), getRoomName(roomId), 'game')
    
    # CURRENT ROOM: Gibt den Raumtext nochmal aus
    elif intentID == 5:
        return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

    # ABOUT: Beantwortet Fragen zum Chatbot
    elif intentID == 6:
        return (aboutHandler(msg), getRoomName(roomId), 'game')
    
    # START PHONE: Der Handymodus wird gestartet
    elif intentID == 7:
        if database.get_user_state_value(username, 'gotPhone') == True:
            return ('You are now chatting with the professor', getRoomName(roomId), 'phone')

    # HELP ASSISTANT
    elif intentID == 8:
        return ('sorry no help assistant yet implemented', getRoomName(roomId), 'game')

    # Wenn nichts erkannt wurde
    return ("I have no idea what you want", getRoomName(roomId), 'game')


"""
@author Max Petendra
@state 10.06.20
get csv file entry
Parameters
----------
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
Returns the csv file entry specified by the input coordinates
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


"""
@author:: Cedric Nehring, Max Petendra
@state: 10.06.20
Check states of room.json in specified category
Parameters
----------
id: the current roomid
name: the category

Returns: a list of tuples by (state, value)
"""


# Prüft alle angesprochenen(roomType) Zustände eines Raumes. Wenn einer nicht zutrifft wird False zurückgegeben.
def checkNeededStates(roomElem, username: str):
    allTrue = True

    for needState, needStateValue in zip(roomElem['needStates'], roomElem['needStatesValue']):
        if None not in (needState, needStateValue) and database.get_user_state_value(username, needState) != needStateValue:
            allTrue = False

    return allTrue

def updateStates(roomElem, username: str):
    
    for newState, newStateValue in zip(roomElem['newStates'], roomElem['newStatesValue']):
        if None not in (newState, newStateValue) and newStateValue:
            database.update_user_state(username, newState, 1)
        elif None not in (newState, newStateValue) and not newStateValue:
            database.update_user_state(username, newState, 0)


def checkNeededItems():
    return True
"""
@author:: Kristin Wünderlich
@state: 17.06.20
Does an action described in the room.json triggers
Parameters
----------
actionName: Name of the action that should be done
actionParam: Parameter for that action
roomId: Id of current room
username: Name of user

Returns: (roomID, game mode)
"""
def doAction(actionName, actionParam, roomId, username):
    actions = {
        "changeMode" :1,
        "addItem" :2,
        "removeItem" :3,
        "changeLocation" :4
    }
    actionId = actions.get(actionName, -1)
    
    #Action not recognized
    if actionId == -1:
        print("This action doesn't exist: "+actionName)
        return (None,None)

    #Change the mode
    elif actionId == 1:
        print("Change the mode to "+actionParam)
        return (None, actionParam)
    
    #Add an item    
    elif actionId == 2:
        print("This item is added: "+actionParam)
        add_to_inventory(actionParam, roomId, username)
        return (None,None)
    
    #Remove an item    
    elif actionId == 3:
        print("This item is deleted: "+actionParam)
        remove_from_inventory(actionParam, roomId, username)
        return (None,None)

    #Changes the room of the player
    elif actionId == 4:
        print("The player moves to room no.: "+ actionParam)
        return(actionParam, None)


"""
@author Max Petendra
@state 10.06.20
handles about questions
Parameters
----------
msg = the user message

Returns a answer for the interrogative fo the player
"""


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
        return "of course not"
    else:
        return "I didnt understand your about chatbot: question."


# inventory stuff
def add_to_inventory(item_name: str, room_ID, username):
    database.insert_item(username, room_ID, item_name)


def remove_from_inventory(item_name: str, room_ID, username):
    database.delete_user_item(username, item_name, room_ID)


def get_inventory(room_ID_0, username) -> str:
    #items == list of tuples

    items_db = database.get_all_user_items(username)

    if items_db is None:
        return "Your Inventory is empty"

    item_str = "Your inventory contains: "
    index = 0
    size = len(items_db)
    l.log_time("items_number: " + str(size))  # logging
    for i in items_db:
        item_name ,room_ID_1 = i
        if index == 0:
            item_str = item_str + item_name
        elif index < size-1:
            item_str = item_str + ", " + item_name
        elif index == size-1:
            item_str = item_str + " and " + item_name
        else:
            item_str = item_str + " ERROR!!! " + item_name
            
        index += 1
        
    return item_str
