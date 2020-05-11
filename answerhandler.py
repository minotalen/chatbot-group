import json
import csv

def answerHandler(inputjson):
    obj = json.loads(inputjson)

    sender = "Chatbot"
    
    answer = findAnswer(str(obj['message']), getRoomId(str(obj['room'])))

    #json wird wieder zusammen gepackt
    fun = json.dumps({"level": 1,"sender": sender,"room":answer[1],"items":[],"message": answer[0]})                    
    return fun


#finds an answer to your message :)
def findAnswer(msg, roomid):
    
    if classifyIntent(msg) == 1:
        for elem in findEntry(roomid, 4).split(';'):
            if msg in elem.split('?')[0]:
                roomid = elem.split('?')[1]
                return (getRoomIntroduction(elem.split('?')[1]),getRoomName(roomid))
    elif classifyIntent(msg) == 2:
         return (getRoomDescription(roomid), getRoomName(roomid))
    else:
        for elem in findEntry(roomid, 3).split(';'):
            if msg in elem.split('?')[0]: return (elem.split('?')[1], getRoomName(roomid))

    return ("I have no idea what you want",getRoomName(roomid))



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

    print(rooms)

    #necessary since we want specific int coordinates not slices
    if not isinstance(id, int) or not isinstance(column, int):
        raise ValueError("Parameter must be of type int")

    if not len(rooms) > id >= 0 or not len(rooms[id]) > column >= 0:
            return "csv table coordinates are out of range"
    else :
        return rooms[id][column]
   

#Get the room id by room name
def getRoomId(msg):
    for i in len(rooms[id]):
        if getRoomName(i) in msg: return findEntry(i,0)
    else: return -1

#Get the current room
def getRoomName(id):
    return findEntry(id, 1)

#Get introduction of the room with id    
def getRoomIntroduction(id):
    return findEntry(id, 2)

#Get description of the room with id
def getRoomDescription(id):
    return findEntry(id, 5)

#Classifies the messages "msg" into 3 different intents
def classifyIntent(msg):
    if "go to" in msg : return 1
    elif "!look around" in msg: return 2
    else: return 3
