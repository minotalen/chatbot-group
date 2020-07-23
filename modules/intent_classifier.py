from fuzzywuzzy import fuzz, process

# intents with synonyms
standard_intent_dic = {
    "inventory": ["inventory", "open inventory","see items","look at inventory","all items","look at items"],
    "look at": ["look around","look at","look","glance","inspect"],
    "go to": ["go to","go","walk","run","move","bounce","hike","jump","enter","sneak"],
    "start": ["start","use","open","turn on","activate"],
    "pick up": ["pick up","take","collect"],
    "current room": ["current room"]
  }

"""
@authors:: Jakob Hackstein, Kevin Katzkowski, Cedric Nering, Kristin Wünderlich
@state:: 23.07.2020
Returns the intent triggered by the classified message. 
"""
def classifyMessage(msg: str, intent_dict: dict=standard_intent_dic) -> str:
    # filter not valid characters from message
    msg = filterMessage(msg)

    for synonym_key, synonym_list in intent_dict.items():
        # check for word matching with fuzzy
        best_match = process.extractOne(msg, synonym_list, scorer=fuzz.partial_ratio)
        print(best_match)

        # only return if input matches partially with at least 90% 
        if best_match[1] >= 90:
            return str(synonym_key)
    return -1


"""
@author:: Max Petendra
@state: 08.06.20
filters a string and only alphabethical char and spaces remain
Parameters:
msg : a string to filter
Returns: the filtered string
"""
def filterMessage(msg: str) -> str: return "".join([ c.lower() for c in msg if c.isalpha() or c == ' ' ])










