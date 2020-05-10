import json
import csv

def anwerHandler(json):
    with open('example.json', 'r') as myfile:
        data = myfile.read()
        obj = json.loads(data)

    room, msg = int(obj['room']), str(obj['msg'])

    switch(classifyIntent(msg)):
        case 1:
            for elem in findentry(room, 4).split(';'):
                if msg in elem.split('?')[0]:
                    #changeRoom(session, getRoomId(msg))
                    return getRoomIntroduction(elem.split('?')[1])

        case 2: return getRoomDescription(room)

        default:
            for elem in findentry(room, 3).split(';'):
                if msg in elem.split('?')[0]: return elem.split('?')[1]

    return "I have no idea what you want"

"""
Returns the csv file entry specified by the input coordinates
id = row / which represent a room
column = column / which represent a property of the rooms
@throws ValueError if parameters ar not of type int
"""
def findentry(id, column):
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
    else if "!look around" in msg : return 2
    else: return 3






"""
c pseudocode idea


answerBot
{
    checkMessage(JSON){
    //Json auseinander nehmen, raum und so
    /Irgendwann müssen wir json ja auch zusammenpacken... egal
    room = json.room;
    msg = json.msg;
    string answer;
    List triggers;

    if(msg.includesSubstring("!go to"){

         for each(room in connection){

             if(msg.includesSubstring(room)){

             //case go to room: Es wird in einen neuen raum gegangen
                 findRoomInCsv(room);
                 changeRoom(session,room);
                 answer = getRoomIntroduction(room);
                 return answer;
             }
         }

    }else if(msg.includesSubstring("!look around")){

    //case look around
        return getRoomDescription(room);

    }else{

        for each(trigger in triggers){

        //Case trigger: Raumspezifischer trigger wurde erkannt
            if(msg.includesSubstring(trigger)){
                answer = getTextForTrigger(room,trigger);
                return answer;
            }
        }

        //case error: nachricht wurde nicht erkannt
        answer = "I have no idea what you want";
        return answer;

    }


    }
}
"""
