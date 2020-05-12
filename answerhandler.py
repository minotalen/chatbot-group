import json
import csv
import pandas as pd
from pathlib import Path


def answerHandler(inputjson):

    obj = json.loads(inputjson)

    sender = "bot"

    answer = findAnswer(str(obj['message']), getRoomId(str(obj['room'])))

    # json wird wieder zusammen gepackt
    return json.dumps({"level": 1, "sender": sender, "room": answer[1], "items": [], "message": answer[0]})


# finds an answer to your message :)
def findAnswer(msg, roomid=-1):
    if roomid == -1 or not isinstance(roomid, int):
        raise ValueError("Invalid room id!")
    checkMessage(msg)

    if classifyIntent(msg) == 1:
        for elem in findEntry(roomid, 4).split(';'):
            print(elem.split('?')[0])
            if elem.split('?')[0] in msg:
                roomid = int(elem.split('?')[1])
                return (getRoomIntroduction(roomid), getRoomName(roomid))

    elif classifyIntent(msg) == 2:
        return (getRoomDescription(roomid), getRoomName(roomid))

    elif classifyIntent(msg) == 4:
        return (get_inventory(), getRoomName(roomid))

    else:
        for elem in findEntry(roomid, 5).split(';'):
            if elem.split('&')[0] in msg:
                return (elem.split('&')[1], getRoomName(roomid))

    return ("I have no idea what you want", getRoomName(roomid))


"""
Returns the csv file entry specified by the input coordinates
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
"""


def findEntry(id, column):

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'roomsGW2.csv'
    file = file_location.open()

    with open(file_location, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='$')
        rooms = [row for row in reader]
    # necessary since we want specific int coordinates not slices
    if not isinstance(id, int) or not isinstance(column, int):
        raise ValueError("Parameter must be of type int")

    if not len(rooms) > id >= 0 or not len(rooms[id]) > column >= 0:
        return "csv table coordinates are out of range"
    else:
        return rooms[id][column]


# Get the room id by room name
def getRoomId(msg):

    checkMessage(msg)

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'roomsGW2.csv'
    file = file_location.open()

    with open(file_location, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='$')
        rooms = [row for row in reader]

    for count in range(0, len(rooms)):

        if rooms[count][1] in msg:
            return int(findEntry(count, 0))
    else:
        return -1

# Get the current room


def getRoomName(id):
    return findEntry(id, 1)

# Get introduction of the room with id


def getRoomIntroduction(id):
    return findEntry(id, 2)

# Get description of the room with id


def getRoomDescription(id):
    return findEntry(id, 3)

# Classifies the messages "msg" into 3 different intents


def classifyIntent(msg):
    if "go to" in msg:
        return 1
    elif "look around" in msg:
        return 2
    elif "items" in msg:
        return 4
    else:
        return 3

# Check if Msg is a String


def checkMessage(msg):
    if not isinstance(msg, str):
        raise ValueError("Message must be of type string")

# manages a local saved inventory
# if "items" in s:

def get_inventory():
    with open("inventory.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0
        item_count = 0
        data = ""
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            if row["Found"] == "True":
                if item_count == 1:
                    data += " and "
                data += str(row["Item-Name"]) + ", " + str(row["Description"])
                item_count = 1
        if item_count == 1:
            data += ". "
        else:
            data = "A yawning void looks at you from your inventory. "
        return data
        
#adds a items to the inventory(sets the variable of the item from 'False' to 'True')
#optional: add a quantity column in the csv

def add_inventory(name):
    with open("inventory.csv") as csvfile:
        df = pd.read_csv("test.csv")
        #df.head(3) #prints 3 heading rows
        df.loc[df["Item-Name"]==name, "Found"] = "True"
        #next line is not tested!
        #df.loc[df["Item-Name"]==, "Item-Quantity"] = ([df["Item-Name"]==, "Item-Quantity"] +1)
        df.to_csv("inventory.csv", index=False)