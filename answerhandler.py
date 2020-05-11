import json
import csv

def answerHandler(json):
    with open('example.json', 'r') as myfile:
        data = myfile.read()
        obj = json.loads(data)

    room, msg = int(obj['room']), str(obj['message'])

    if classifyIntent(msg) == 1:
        for elem in findEntry(room, 4).split(';'):
            if msg in elem.split('?')[0]:
                #changeRoom(session, getRoomId(msg))
                return getRoomIntroduction(elem.split('?')[1])
    elif classifyIntent(msg) == 2:
        return getRoomDescription(room)
    else:
        for elem in findEntry(room, 3).split(';'):
            if msg in elem.split('?')[0]: return elem.split('?')[1]

    return "I have no idea what you want"

"""
Returns the csv file entry specified by the input coordinates
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
"""
def findEntry(id, column):
    with open('rooms.csv', 'r') as file:
        reader = csv.reader(file)
        rooms = [row for row in reader]

    #necessary since we want specific int coordinates not slices
    if not isinstance(id, int) or not isinstance(column, int):
        raise ValueError("Parameter must be of type int")

    if not len(rooms) > id >= 0 or not len(rooms[id]) > column >= 0:
            return "csv table coordinates are out of range"
    else :
        return rooms[id][column]

def changeRoom(session, room):
    pass

def enterRoom():
    pass

def getRoomId(msg):
    pass

def getRoomIntroduction():
    return "Hallo ich bin eine Einleitung"

def getRoomDescription(id):
    return "Hallo ich bin ein Raum"

def classifyIntent(msg):
    if "go to" in msg : return 1
    elif "!look around" in msg: return 2
    else: return 3
