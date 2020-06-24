import json
import database_SQLite as database
from intentclassificator import classifyIntent




# open json for messages from prof
with open('gps.json', encoding="utf8") as gps:
    rec_json = json.load(gps)
    locations = rec_json['locations']


def handleGPS(msg: str, username:str, level:int, roomId:int = -1):
    if roomId == -1 : raise ValueError("Invalid Room Id Parameter")
    else: resultRoomId = -1

    intentID = classifyIntent(msg, ["go to"])
    if intentID == 1:
        possibleLocations = getPossibleLocations(username)
        intentID = classifyIntent(msg, possibleLocations)
        if intentID != -1: 
            for location in locations:
                if location.get("locationName") == possibleLocations[intentID-1]:
                    resultRoomId = location.get("StartRoomId")

    if resultRoomId == roomId: return ("You are already at this location", roomId, 'game') 
    if resultRoomId != -1: return ("You have beamed to your choosen location", resultRoomId, 'game')       
    return ("Your location has not been changed. Try again or exit gps.", roomId, 'gps')




def getPossibleLocations(username: str) -> list:
    return [location.get("locationName") for location in locations if all(list(map(lambda x: database.get_user_state_value(username, x, False), location.get("neededStates"))))]




def printLocations(username: str) -> str:
     return "You can beam yourself to:<br>" + '<br>'.join(getPossibleLocations(username))
