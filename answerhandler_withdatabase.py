import database_noSQL as database
import json
import pandas as pd
from pathlib import Path
from intentclassificator import classifyIntent, writeMessagetoTrainingData


def answerHandler(inputjson):
    obj = json.loads(inputjson)

    sender = "bot"
    answer = findAnswer(str(obj['message'].lower()), getRoomId(str(obj['room'])))

    if writeMessagetoTrainingData(str(obj['message'])):
        print("added message to training data")
    else:
        print("added nothing to training data")

    # json wird wieder zusammen gepackt
    return json.dumps({"level": 1, "sender": sender, "room": answer[1], "items": [], "message": answer[0]})


# finds an answer to your message :)
def findAnswer(msg, roomid=-1):
    all_of_data = database.roomsGW2_collection.find()
    if roomid == -1:
        raise ValueError("Invalid room id!")

    # all_of_rooms = database.collection.find({"connection"})
    # if classifyIntent(msg) == 1:
    #     for room in all_of_rooms:

    if classifyIntent(msg) == 1:
        for results in all_of_data:
            temp = results['connections']
            for result in temp:
                if result in msg:
                    roomid = temp[result]
                    return getRoomIntroduction(roomid), getRoomName(roomid)

    elif classifyIntent(msg) == 2:
        return getRoomDescription(roomid), getRoomName(roomid)

    elif classifyIntent(msg) == 3:
        return getRoomIntroduction(roomid), getRoomName(roomid)

    elif classifyIntent(msg) == 4:
        return get_inventory(), getRoomName(roomid)
    elif classifyIntent(msg) == 5:
        return aboutHandler(msg), getRoomName(roomid)
    else:
        for results in all_of_data:
            temp = results['triggers']
            for result in temp:
                if result in msg:
                    answer = temp[result]
                    return answer, getRoomName(roomid)

    #     else:
    #         for elem in findEntry(roomid, 5).split(';'):
    #             if elem.split('&')[0] in msg: return elem.split('&')[1], getRoomName(roomid)

    return "I have no idea what you want", getRoomName(roomid)


def getRoomId(msg):
    all_of_data = database.roomsGW2_collection.find()
    for data in all_of_data:
        if data["room_name"] in msg:
            return data["_id"]
    else:
        return -1


# Get the current room
def getRoomName(id):
    return findEntry(id, "room_name")


# Get introduction of the room with id
def getRoomIntroduction(id):
    return findEntry(id, "introduction")


# Get description of the room with id
def getRoomDescription(id):
    return findEntry(id, "description")


def findEntry(id, room_name):
    results = database.roomsGW2_collection.find({"_id": id})
    count = database.roomsGW2_collection.count()
    for result in results:
        doc = result[room_name]

    if not isinstance(id, int):
        raise ValueError("Parameter id must be of type int")
    if not isinstance(room_name, str):
        raise ValueError("Parameter room_name must be of type str")
    if not count > id >= 0:
        return "the id is out of range"
    else:
        return doc


# Handles about questions
def aboutHandler(msg):
    if "who has" in msg:
        return "I am programmed by student members of the Chatbots:Talk-To-Me Team"
    elif "who are" in msg:
        return "I am a Chatbotgame with a browser interface"
    elif "why are" in msg:
        return "I was born because the virtualmarsexplporation Project has not enought places for all the students"
    elif "when did" in msg:
        return "I was born during the summer semester of 2020"
    elif "what are" in msg:
        return "I want to deliver fun and interesting facts about Bremen"
    elif "where are" in msg:
        return "I was programmed in Bremen"
    else:
        return "I didnt understand your about chatbot: question."


# Check if Msg is a String
def checksMessage(msg):
    if not isinstance(msg, str):
        raise ValueError("Message must be of type string")


def get_inventory():
    inventories = database.inventory_collection.find()
    item_count = 0
    data = ""
    for item in inventories:
        if item["found"] == "True":
            if item_count == 1:
                data += " and "
            data += item["Item-Name"] + ", " + item["Description"]
            item_count = 1
    if item_count == 1:
        data += ". "
    else:
        data = "A yawning void looks at you from your inventory. "
    return data
