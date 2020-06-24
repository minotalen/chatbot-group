import json
import database_SQLite as database



"""
@author:: Cedric Nering, Max Petendra
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


def checkNeededItems(roomElem, username: str):
    allTrue = True

    for needItem, needItemRoomId in zip(roomElem['needItems'], roomElem['needItemsRoomId']):
        if None not in (needItem, needItemRoomId) and not database.does_user_item_exist(username, needItem, needItemRoomId):
            allTrue = False

    return allTrue

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
        "changeLocation" :4,
        "changeSender" :5
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
        print("The player moves to room no.: "+ str(actionParam))
        return(actionParam, None)
    
    #Changes the sender of the message
    elif actionId == 5:
        print("The Sender's name is now: " + str(actionParam))
        return(None, None, actionParam) 
    

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

