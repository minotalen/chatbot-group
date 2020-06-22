import json
import database_SQLite as database

with open('rooms.json', encoding="utf8") as allLevels:
    data = json.load(allLevels)
    rooms = data['rooms']





#returns (roomId, game mode)
def doAction(actionName, actionParam, roomId, username):
    actions = {
        "changeMode" :1,
        "addItem" :2,
        "removeItem" :3,
        "changeLocation" :4
    }
    actionId = actions.get(actionName, -1)

    print (rooms[roomId][])
    
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
        
