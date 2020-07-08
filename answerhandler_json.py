import json
import pandas as pd
import database_SQLite as database
import data_json_functions as djf
from gps import handleGPS, printLocations
from nltk import tokenize
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData
from phone import handleAnswer, getSizeofMessagequeue, get_generated_answer, formatHTMLText
from riddlemode import checkAnswer
import logging_time as l
import audio as audio

with open('rooms.json', encoding="utf8") as allLevels:
    data = json.load(allLevels)
    rooms = data['rooms']


"""
@author Max Petendra
others please write your name to authors if you have done something
@state 22.06.20
handles the json input and output // speaks to specific answerHandlers of the game modes
Parameters
----------
inputjson: the json from the server
username: the username of the user currently playing

Returns the json from the client
"""


def answerHandler(inputjson, username):
    l.log_start()  # logging
    obj = json.loads(inputjson)

    # When the mode is phone and player inputs exit phone
    if str(obj['mode']) == 'phone' and classifyIntent(str(obj['message'].lower()), ['exit phone']) == 1:
        answer = ('You stop looking at the bad quality of your phone',
                  getRoomName(getRoomId(str(obj['room']))), 'game')

    # When the mode is phone
    elif str(obj['mode']) == 'phone':
        answer = [handleAnswer(str(obj['message'].lower()), username, int(obj['level']), getRoomId(
            str(obj['room']))), getRoomName(getRoomId(str(obj['room']))), 'phone']

      # When the mode is gps and player inputs exit gps
    elif str(obj['mode']) == 'gps' and classifyIntent(str(obj['message'].lower()), ['exit gps']) == 1:
        answer = ('Your gps device is now turned off',
                  getRoomName(getRoomId(str(obj['room']))), 'game')

    # When the mode is gps
    elif str(obj['mode']) == 'gps':
        cur_room_id = getRoomId(str(obj['room']))
        gpsTriple = handleGPS(str(obj['message'].lower()), username, int(
            obj['level']), getRoomId(str(obj['room'])))
        if cur_room_id == gpsTriple[1]:
            answer = [
                gpsTriple[0], getRoomName(gpsTriple[1]), gpsTriple[2]]
        else:
            answer = [
                gpsTriple[0] + "<br>" + getRoomIntroduction(gpsTriple[1]), getRoomName(gpsTriple[1]), gpsTriple[2]]

    # When the mode is riddle
    elif str(obj['mode']) == 'riddle':
        answer = checkAnswer(str(obj['message'].lower()), getRoomId(
            str(obj['room'])), username)
        answer[1] = getRoomName(answer[1])

    # When mode is game
    else:
        #l.log_time('remove_tables')
        #database.remove_unused_tables()
        answer = findAnswer(username, str(
            obj['message'].lower()), getRoomId(str(obj['room'])))

    if writeMessagetoTrainingData(str(obj['message'])):
        print("added message to training data")
    else:
        print("added nothing to training data")

    #text to spreech if it is turned on in the setting @author Max Petendra
    if json.loads(get_settings_by_username(username))['readMessages']: audio.playSound(answer[0])
        
    
    
    # json wird wieder zusammen gepackt
    l.log_time('end')  # logging
    l.log_end()  # logging


    #Check if a differnt sender is given
    if len(answer) <= 3:newSender = "bot"
    else:newSender = answer[3]
        

    
    return json.dumps(
        {"level": 1, "sender": newSender, "room": answer[1], "items": [], "mode": answer[2], "message": answer[0]})
        


"""
@author Max Petendra
other pleasse write your name to authors if you have done something
@state 23.06.20
handles the logic in mode game
checks triggers, then intents and otherwise returns default answer
Parameters
----------
username: the name of the current user playing the game
msg = the user message
roomId = the current id of the room the player is in (default = -1 if no id is given)

Returns a triple if the reply message of the chatbot the room id and the 
"""


def findAnswer(username, msg, roomId=-1):
    if roomId == -1:
        raise ValueError("Invalid room id!")

    choices = ["go to", "look at", "pick up", "items", "current room",
               "about chatbot:", "start phone", "start gps", "help assistant:"]

    elemCount = -1
    # TRIGGER: Raumspezifische Trigger werden zuerst überprüft // please write docs in english :''(
    for elem in rooms[roomId]['triggers']:
        if elem is not None:
            elemCount += 1
            if elem['trigName'] in msg and djf.checkNeededStates(rooms[roomId]['triggers'][elemCount],
                                                                 username) and djf.checkNeededItems(rooms[roomId]['triggers'][elemCount], username):

                djf.updateStates(rooms[roomId]['triggers']
                                 [elemCount], username)

                altMode = 'game'
                altRoom = roomId
                altSender ='bot'
                if elem['actions'][0] is not None:
                    for action, actionValue in zip(elem['actions'], elem['actionsValue']):
                        altAction = djf.doAction(
                            action, actionValue, roomId, username)
                        if altAction[0] is not None:
                            altRoom = altAction[0]
                        elif altAction[1] is not None:
                            altMode = altAction[1]
                        elif altAction[2] is not None: altSender = altAction[2]

                return (elem['accept'], getRoomName(altRoom), altMode, altSender)
            
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
                if name in msg and djf.checkNeededStates(rooms[roomId]['connections'][elemCount], username):
                    roomId = int(elem['conRoomId'])

                    return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

        elemCount = -1
        # OBJEKTE
        for elem in rooms[roomId]['objects']:
            elemCount += 1

            if elem['objName'] in msg and djf.checkNeededStates(rooms[roomId]['objects'][elemCount], username):
                djf.updateStates(rooms[roomId]['objects'][elemCount], username)

                return (elem['lookAt'], getRoomName(roomId), 'game')

    # LOOK AT: Items und Objekte im Raum können angeschaut werden. ansonsten wird LOOK AROUND die Raumbeschreibungs ausgegeben
    elif intentID == 2:
        elemCount = -1
        # ITEMS
        if rooms[roomId]['items'][0] is not None:
            for elem in rooms[roomId]['items']:
                elemCount += 1

                if elem['itemName'] in msg and djf.checkNeededStates(rooms[roomId]['items'][elemCount], username):

                    return (elem['lookAt'], getRoomName(roomId), 'game')
        
        # INThere is a bench, a trash bin and a strange looking bush near the monument. You also notice a small staircase leading below the base of the monument.On a side view you can see a number of buildings surrounding the monuments. If you take a look at the left-hand side of the stairs, you will see only two other building. In the center is the stone shrine. If you look at the left-hand side of the stairs, you can see the same side. There's a great view from here. At the top of the stairs, you can see several wooden crosses. The second thing you see while looking up is something very peculiar. If you look at the left-hand side of each picture, you will see an enormous structure that resembles the pyramid of Saturn.VENTORY
        for i in database.get_all_user_items(username):
            if i[0] in msg:
                for elem in rooms[i[1]]['items']:
                    if elem['itemName'] == i[0]:
                        return (elem['lookAt'], getRoomName(roomId), 'game', 'inventory')

        elemCount = -1
        # OBJEKTE
        if rooms[roomId]['objects'][0] is not None:
            for elem in rooms[roomId]['objects']:
                elemCount += 1

                if elem['objName'] in msg and djf.checkNeededStates(rooms[roomId]['objects'][elemCount], username):
                    djf.updateStates(
                        rooms[roomId]['objects'][elemCount], username)

                    return (elem['lookAt'], getRoomName(roomId), 'game')

        if json.loads(get_settings_by_username(username))['gpt2Output']:
            # room discription from json
            raw_desc_sentences = tokenize.sent_tokenize(formatHTMLText(getRoomDescription(roomId))) 

            # take last 3 sentences from input
            if len(raw_desc_sentences) > 3 : raw_desc_sentences = raw_desc_sentences[-3:]
            raw_desc_sentences = " ".join(raw_desc_sentences)

            # with a generated text added by gpt2 on context of the room discription 
            gen_description = getRoomDescription(roomId) + ' ' + get_generated_answer(raw_desc_sentences, 55)

            return (gen_description, getRoomName(roomId), 'game')
        else:
            return (getRoomDescription(roomId), getRoomName(roomId), 'game') 

    # PICK UP: Hebt ein item auf und gibt den Text zurück
    elif intentID == 3:
        if rooms[roomId]['items'][0] is not None:
            elemCount = -1
            for elem in rooms[roomId]['items']:
                elemCount += 1

                if elem['itemName'] in msg and djf.checkNeededStates(rooms[roomId]['items'][elemCount], username):
                    djf.updateStates(rooms[roomId]['items'][elemCount], username)
                    djf.add_to_inventory(elem['itemName'], roomId, username)

                    return (elem['pickUp'], getRoomName(roomId), 'game')

    # ITEMS: NOCH NICHT FERTIG. BAUSTELLE
    elif intentID == 4:
        return (djf.get_inventory(roomId, username), getRoomName(roomId), 'game', 'inventory')

    # CURRENT ROOM: Gibt den Raumtext nochmal aus
    elif intentID == 5:
        return (getRoomIntroduction(roomId), getRoomName(roomId), 'game')

    # ABOUT: Beantwortet Fragen zum Chatbot
    elif intentID == 6:
        return (aboutHandler(msg), getRoomName(roomId), 'game')

    # START PHONE: Der Handymodus wird gestartet
    elif intentID == 7:
        if database.get_user_state_value(username, 'solvedPinCode') == True:
            return ('Phone started  <em>Type manual to open usage instructions</em><br>You are now chatting with the professor. <br>' + 'You have ' + str(getSizeofMessagequeue(username)) + ' new messages in your mailbox', getRoomName(roomId), 'phone')

    # START GPS DEVICE
    elif intentID == 8:
        if database.get_user_state_value(username, 'ownGps') == True:
            return (printLocations(username), getRoomName(roomId), 'gps')

    # HELP ASSISTANT
    elif intentID == 9:
        return ('sorry no help assistant yet implemented', getRoomName(roomId), 'game')

    # Wenn nichts erkannt wurde
    return ("I have no idea what you want", getRoomName(roomId), 'game')


"""
@author Max Petendra
@state 10.06.20
returns roomid from json
Parameters
----------
roomName : the roomName the player wants to know the id from

Returns the roodId specified by the room name (-1 if no roodId is found)
"""


def getRoomId(roomName: str) -> int:
    for count in range(0, len(rooms)):
        if rooms[count]['roomName'] in roomName:
            return int(rooms[count]['id'])
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

#@author Canh Dinh, Kevin
def get_settings_by_username(username: str):
    if database.does_setting_exist(username):
        data = database.find_settings_by_username(username)
        initial_data = {"username": data[1], "json": data[2]}
        #print(data[2])
        json_string = data[2]
        # json_data = json.dumps(json_string[1:])
        return json_string
    else:
        print('user does not exist')




"""
@author Max Petendra
@state 10.06.20
handles about questions
Parameters
----------
msg = the user message

Returns a answer for the interrogative of the player
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
