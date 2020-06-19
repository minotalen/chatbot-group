import json
import database_SQLite as database
import data_json_functions as djf

helpText = "Hello dear adventurer! You are currently in riddle mode. Your quest is to type the right answer to continue the game. If you want to leave the riddle mode to continue exploring the world, please type 'go back' or 'exit'"

#Beim öffnen der .py wird die Rätsel JSON geladen
with open('riddle.json', encoding="utf8") as allRiddles:
    data = json.load(allRiddles)
    riddles = data['rooms']
    newMode ="riddle"
    
#Handler der Klasse, nimmt eine JSON und gibt einen tupel wieder [antwort, modus]    
def handleRiddle(inputjson):
    
    obj = json.loads(inputjson)
    answer = checkAnswer(str(obj["message"]), int(obj["room"]))

    return answer

#Ergebnisse können sein: richtig, falsch, abbruch, beschreibung, help
def checkAnswer(msg, roomId, username) -> str:

    riddleId = getRiddleId(roomId)
    
    rightAnswer = riddles[riddleId]['rightAnswer']
    rightText = riddles[riddleId]['rightText']
    falseText = riddles[riddleId]['falseText']
    
    if rightAnswer == msg :
        djf.updateStates(riddles[riddleId],username)
        altRoom = roomId
        if riddles[riddleId]['actions'][0] is not None:
            for action, actionValue in zip(riddles[riddleId]['actions'], riddles[riddleId]['actionsValue']):
                altAction = djf.doAction(action, actionValue, roomId, username)
                if altAction[0] is not None: altRoom = altAction[0]
        
        return [rightText, altRoom, "game"]
    
    elif "help" in msg :return [helpText, roomId, "riddle"]
    elif "what" in msg: return [riddles[riddleId]['descri'], roomId, "riddle"]
    elif "go back" in msg or "exit" in msg:
        return ["You leave this riddle for now and return back to reality", roomId,"game"]
    else : return [falseText, roomId, "riddle"]
  
def getRiddleId(roomId):       
    # getting length of list 
    length = len(riddles) 
   
    # Iterating the index 
    # same as 'for i in range(len(list))' 
    for i in range(length): 
        if(riddles[i]['roomId'] == roomId): return i
        
    return -1



