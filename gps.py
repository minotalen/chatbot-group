import json
import database_SQLite as database
from intentclassificator import classifyIntent

# open json for messages from prof
with open('gps.json', encoding="utf8") as gps:
    rec_json = json.load(gps)
    locations = rec_json['locations']


"""
@author:: Max Petendra, Jakob Hackstein
@state: 24.06.20
handle all messages for the gps

Parameters
----------
msg: the message of the user
username: the username of the user
level: level of the game
roomId: current room id

Returns: triple containing (msg, new roomID, new gamemode)
"""
def handleGPS(msg: str, username: str, level: int, roomId: int = -1):
    if roomId == -1: raise ValueError("Invalid Room Id Parameter")
    else: resultRoomId = -1

    intentID = classifyIntent(msg, ["go to", "print locations"])
    print("intentID", intentID)
    if intentID == 1:
        possibleLocations = getPossibleLocations(username)
        intentID = classifyIntent(msg, possibleLocations)
        if intentID != -1:
            for location in locations:
                if location.get("locationName") == possibleLocations[intentID - 1]:
                    resultRoomId = location.get("startRoomId")

    elif intentID == 2:
        return (printLocations(username), roomId, 'gps')

    # if location has not changed -> stay in gps mode
    if resultRoomId == roomId:
        return ("You are already at this location", roomId, 'gps')

    # if location has changed -> change loc, exit gps mode, play intro text
    if resultRoomId != -1:
        return ("You have beamed to your choosen location and turned off your gps.", resultRoomId, 'game')

    # if classifier failed
    return ("Your location has not been changed. Try again or exit gps.", roomId, 'gps')


"""
@author:: Max Petendra
@state: 24.06.20
get all possible locations for the user

Parameters
----------
username: the current username

Returns: list of strings, possible locations
"""
def getPossibleLocations(username: str) -> list:
    return [location.get("locationName") for location in locations if all(list(map(lambda x: database.get_user_state_value(username, x, False), location.get("neededStates"))))]


"""
@author:: Max Petendra, Jakob Hackstein
@state: 24.06.20
print all location in with HTML line break

TODO split answer into two messages

Parameters
----------
username: the current username

Returns: a string containing all possible locations
"""
def printLocations(username: str) -> str:
    return "You can beam yourself to:<br>" + '<br>'.join(getPossibleLocations(username))
