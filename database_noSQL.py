from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://elephanture:1234@cluster0-yn22k.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["elephanture"]

roomsGW2_collection = db["roomsGW2"]

roomsGW2_post = {
    "_id": 0,
    "room_name": "Introduction",
    "introduction": "Welcome to our prototype of a text adventure that is currently in development. For now you can "
                    "only play for a few steps but more stuff will be included later on! With 'look around' you will "
                    "get more insights on how to start the game.$You can start the prototype with the command 'go to "
                    "start'. <br>You should also consider the following commands to be able to play the game as it is "
                    "meant to be. <br>'go to ROOM'  You can go to any said room or direction <br>'pick up OBJECT'  "
                    "You can pick up any said object inside of the current room <br>'open OBJECT'  You can open said "
                    "object <br>'use OBJECT'  You can use the named object for or with something inside of the "
                    "current room <br>'current room'  Gives you the name of the current room you are in and the "
                    "introduction text of it",
    "description": "You can start the prototype with the command 'go to start'. <br>You should also consider the "
                   "following commands to be able to play the game as it is meant to be. <br>'go to ROOM'  You can go "
                   "to any said room or direction <br>'pick up OBJECT'  You can pick up any said object inside of the "
                   "current room <br>'open OBJECT'  You can open said object <br>'use OBJECT'  You can use the named "
                   "object for or with something inside of the current room <br>'current room'  Gives you the name of "
                   "the current room you are in and the introduction text of it",
    "connections": {
        "start": 1
    },
    "triggers": {}
}

roomsGW2_post1 = {
    "_id": 1,
    "room_name": "First Hallway",
    "introduction": "To your right there is a room with a slightly open door. To your left you can go around a "
                    "corner. There is also a locked door to a fire escape.",
    "description": "To your right there is a room with a slightly open door. To your left you can go around a corner. "
                   "There is also a locked door to a fire escape.",
    "connections": {
        "door": 2,
        "right": 2
    },
    "triggers": {
        "use key": "You Wait till no one watches and you put the rusty key in a lock of the fire exit. After "
                   "some poking the door gives up and opens. You jump down the stairs. The door at the end opens far "
                   "smoother than the first one, probably an older one and you're out. Only a few minutes left to get "
                   "to the GW1 where the exam takes place. You have luck, you got a bus waiting for the right "
                   "destination. After the ride you are heading to the front of the GW1. Knowing you are on time "
                   "makes you relieve and you are definitely going to pass the exam.",
    }

}

roomsGW2_post2 = {
    "_id": 2,
    "room_name": "Math Room",
    "introduction": "You walk towards the open door and already feel your math senses tickling. You enter an empty "
                    "room. There is a white board that is filled with weird math formulas, but something kicks in you "
                    "and you sense a key hidden behind the wall of math. If you can solve this complex calculation "
                    "you might be able to reach behind it.",
    "description": "There is a white board that is filled with weird math formulas, but something kicks in you and "
                   "you sense a key hidden behind the wall of math. If you can solve this complex calculation you "
                   "might be able to reach behind it.",
    "connections": {
        "hallway": 1
    },
    "triggers": {
        "solve riddle": "This is written on the white board: <br> <br>You buy a watch for thirty euros. <br>You sell "
                        "it for forty euros. <br>You buy it once again for fifty euros. <br>You sell it once again "
                        "for sixty euros. <br>How much euros did you gain compared to the very beginning? <br> "
                        "<br>There is an empty square on the bottom right which should be the place to write the "
                        "answer",
        "20": "You write the right answer on the board and in the corner of your eye you see a brick on the wall "
              "behind with crumbling mortar. You grab the brick and it gets loose. Behind the brick is a tiny "
              "Matryoshka doll. You open the matryoshka. Inside is an even tinier Matryoshka doll. And inside this "
              "one is a rusty key with a keychain on it. Carved on the keychain are letters that appear random at "
              "first. You scratch the key against the wall to rub the rust off. You rub a bit too hard and shiny "
              "metal breaks out of the rust. Carvings on the metal spell the word 'fire escape'. An idea forms into "
              "your head. If this key is really a key to the fire exit, it would not cause an alarm and you can "
              "swiftly exit the building. So you take your feet in your hands and get the hell out of the room ",
    }

}


def find_all_rooms():
    results = roomsGW2_collection.find()
    for result in results:
        print(result)


def find_room_by_id(room_id, value):
    results = roomsGW2_collection.find({f"_{room_id}": value})
    for result in results:
        print(result)


def count_room():
    result = roomsGW2_collection.count()


def insert_one_room(item):
    roomsGW2_collection.insert_one(item)


def insert_many_rooms(list):
    if not isinstance(list, list):
        ValueError("Using insertManyRecords the input list must be type of list")
    roomsGW2_collection.insert_many(list)


def delete_one_rooms_by_id(room_id, value):
    if not isinstance(id, str):
        ValueError("id must be type of str")
    if not isinstance(value, str) or isinstance(value, int):
        ValueError("value must be type of str or int for key")
    roomsGW2_collection.delete_one({f"_{room_id}": value})


"""
========================================================================================================================
"""

inventory_collection = db["inventory"]

inventory_post = {
    "item_id": "0",
    "item_name": "Stone of Pingu",
    "found": "False",
    "description": "a powerful artifact that gives the wielder the ability to noot noot",
    "": "",
    "notes": ""
}

inventory_post1 = {
    "item_id": "1",
    "item_name": "a wallet of stones",
    "found": "False",
    "description": "its just a wallet that's filled with stones duh",
    "": "",
    "notes": ""
}


def find_all_inventory():
    results = inventory_collection.find()
    for result in results:
        print(result)

# find_room_by_id("id", 2)
# find_all_room()
