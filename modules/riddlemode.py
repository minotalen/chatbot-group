import json
import database_SQLite as database
import data_json_functions as djf

helpText = "Hello dear adventurer! You are currently in riddle mode. Your quest is to type the right answer to continue the game. If you want to leave the riddle mode to continue exploring the world, please type 'go back' or 'exit'"

#Beim öffnen der .py wird die Rätsel JSON geladen
with open('json/riddle.json', encoding="utf8") as allRiddles:
    data = json.load(allRiddles)
    riddles = data['rooms']
    newMode ="riddle"
    
#Ergebnisse können sein: richtig, falsch, abbruch, beschreibung, help
def checkAnswer(msg, roomId, username) -> str:

    riddleId = getRiddleId(roomId)

    if "help" in msg :return [helpText, roomId, "riddle"]
    elif "what" in msg: return [riddles[riddleId]['descri'], roomId, "riddle"]
    elif "go back" in msg or "exit" in msg:
        return ["You leave this riddle for now and return back to reality", roomId,"game"]
    else :
        if riddleId == 0:
            return RiddleZero(msg, roomId, username)
        elif riddleId == 1:
            return RiddleOne(msg, roomId, username)
        else: return ["RiddleId error", roomId, "game"]
  
def getRiddleId(roomId):       
    # getting length of list 
    length = len(riddles) 
   
    # Iterating the index 
    # same as 'for i in range(len(list))' 
    for i in range(length): 
        if(riddles[i]['roomId'] == roomId): return i
        
    return -1

def RiddleZero(msg, roomId, username):
    
    rightAnswer = riddles[0]['rightAnswer']
    rightText = riddles[0]['rightText']
    falseText = riddles[0]['falseText']
    
    if rightAnswer == msg :
        djf.updateStates(riddles[0],username)
        altRoom = roomId
        if riddles[0]['actions'][0] is not None:
            for action, actionValue in zip(riddles[0]['actions'], riddles[0]['actionsValue']):
                altAction = djf.doAction(action, actionValue, roomId, username)
                if altAction[0] is not None: altRoom = altAction[0]
        
        return [rightText, altRoom, "game"]
    
    else: return [falseText, roomId, "riddle"]


def RiddleOne(msg, roomId, username):

    numbermsg = ''.join(filter(str.isdigit, msg))
    if numbermsg != '': numbersonly = int(numbermsg)
    else: numbersonly = -1
    print(numbermsg+ " "+str(numbersonly))

    rightAnswer = riddles[1]['rightAnswer']
    rightText = riddles[1]['rightText']
    falseText = riddles[1]['falseText']


    if rightAnswer == numbermsg :
        djf.updateStates(riddles[1],username)
        altRoom = roomId
        if riddles[1]['actions'][0] is not None:
            for action, actionValue in zip(riddles[1]['actions'], riddles[1]['actionsValue']):
                altAction = djf.doAction(action, actionValue, roomId, username)
                if altAction[0] is not None: altRoom = altAction[0]
        
        return [rightText, altRoom, "game"]

    elif numbersonly == -1: return [falseText, roomId, "riddle"]
    
    elif numbersonly > 20:
        return ["I don't have that much money with me.", roomId, "riddle"]

    elif numbersonly < 5:
        return ["This price is so low, I feel like you insulted my whole family.", roomId, "riddle"]
    
    elif numbersonly < 20:
        return ["This is definetly not enough for this chest. I am not gonna give it as a present.", roomId, "riddle"]


    
    

