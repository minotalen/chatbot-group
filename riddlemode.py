import json

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
def checkAnswer(msg, roomId) -> str:

    riddleId = getRiddleId(roomId)
    
    rightAnswer = riddles[riddleId]['rightAnswer']
    rightText = riddles[riddleId]['rightText']
    falseText = riddles[riddleId]['falseText']
    
    if rightAnswer == msg :
        updateStatus(riddleId)
        return [rightText, roomId, "game"]
    
    elif "help" in msg :return [helpText, roomId, "riddle"]
    elif "what" in msg: return [riddles[riddleId]['descri'], roomId, "riddle"]
    elif "go back" in msg:
        return ["You leave this riddle for now and return back to reality", roomId,"game"]
    elif "exit" in msg:
        return ["You leave this riddle for now and return back to reality", roomId,"game"]
    else : return [falseText, roomId, "riddle"]

#Neue Zustande werden hier zugewiesen, wenn das rätsel erfolgreich war
def updateStatus(RiddleId):
    #ändere zustände auf der datenbank
    pass

    
def getRiddleId(roomId):       
    # getting length of list 
    length = len(riddles) 
   
    # Iterating the index 
    # same as 'for i in range(len(list))' 
    for i in range(length): 
        if(riddles[i]['roomId'] == roomId): return i
        
    return -1
