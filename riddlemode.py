import json

helpText = "Hello dear adventurer! You are currently in riddle mode. Your quest is to type the right answer to continue the game. If you want to leave the riddle mode to continue exploring the world, please type 'go back' or 'exit'"


with open('riddle.json', encoding="utf8") as allRiddles:
    data = json.load(allRiddles)
    riddles = data['rooms']
    newMode ="riddle"
    
def handleRiddle(inputjson):
    
    obj = json.loads(inputjson)
    roomId = int(obj["room"])
    level = int(obj["level"])
    answer = checkAnswer(str(obj["message"]), int(obj["room"]))

    return json.dumps({"level": 1,"sender": "bot","room":roomId,"items":[],"message": answer})

#Ergebnisse können sein: richtig, falsch, abbruch, beschreibung, help
def checkAnswer(msg, roomId) -> str:

    riddleId = getRiddleId(roomId)
    
    rightAnswer = riddles[riddleId]['rightAnswer']
    rightText = riddles[riddleId]['rightText']
    falseText = riddles[riddleId]['falseText']
    
    if rightAnswer == msg :
        endRiddleMode()
        return rightText
    
    elif "help" in msg :return helpText
    elif "what" in msg: return riddles[riddleId]['descri']
    elif "go back" in msg:
        endRiddleMode()
        return "You leave this riddle for now and return back to reality"
    elif "exit" in msg:
        endRiddleMode()
        return "You leave this riddle for now and return back to reality"
    else : return falseText
    
def endRiddleMode():
    newMode = "game"
    
def getRiddleId(roomId):
       
    # getting length of list 
    length = len(riddles) 
   
    # Iterating the index 
    # same as 'for i in range(len(list))' 
    for i in range(length): 
        if(riddles[i]['roomId'] == roomId): return i
        
    return -1
